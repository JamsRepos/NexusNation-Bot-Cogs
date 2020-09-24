import lavalink
import asyncio
import urllib.parse
from abc import ABC
from contextlib import suppress
from io import BytesIO
from operator import itemgetter
from typing import Optional

import aiohttp
import discord
from redbot.core import Config, commands
from redbot.core.data_manager import bundled_data_path
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import escape, pagify
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu

from .charts import charts, track_chart
from .utils import *
from .whoknows import WhoKnowsMixin

with suppress(Exception):
    from wordcloud import WordCloud


async def wordcloud_available(ctx):
    return "WordCloud" in globals().keys()


async def tokencheck(ctx):
    token = await ctx.bot.get_shared_api_tokens("lastfm")
    return bool(token.get("appid"))


class CompositeMetaClass(type(commands.Cog), type(ABC)):
    """This allows the metaclass used for proper type detection to coexist with discord.py's
    metaclass."""


class LastFM(
    UtilsMixin, WhoKnowsMixin, commands.Cog, metaclass=CompositeMetaClass,
):
    # noinspection PyMissingConstructor
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=95932766180343808, force_registration=True)
        defaults = {"lastfm_username": "Bramble2610"}
        self.config.register_global(version=1)
        self.config.register_user(**defaults)
        self.config.register_guild(crowns={})
        self.session = aiohttp.ClientSession(
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Arch Linux; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"
            },
            loop=self.bot.loop,
        )
        self.token = None
        self.wc = None
        if "WordCloud" in globals().keys():
            self.wc = WordCloud(width=1920, height=1080, mode="RGBA", background_color=None)
        self.data_loc = bundled_data_path(self)

    async def initialize(self):
        token = await self.bot.get_shared_api_tokens("lastfm")
        self.token = token.get("appid")
        await self.migrate_config()

    async def migrate_config(self):
        if await self.config.version() == 1:
            a = {}
            conf = await self.config.all_guilds()
            for guild in conf:
                a[guild] = {"crowns": {}}
                for artist in conf[guild]["crowns"]:
                    a[guild]["crowns"][artist.lower()] = conf[guild]["crowns"][artist]
            group = self.config._get_base_group(self.config.GUILD)
            async with group.all() as new_data:
                for guild in a:
                    new_data[guild] = a[guild]
            await self.config.version.set(2)

    @commands.Cog.listener()
    async def on_red_api_tokens_update(self, service_name, api_tokens):
        if service_name == "lastfm":
            self.token = api_tokens.get("appid")

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    @commands.is_owner()
    @commands.command(aliases=["fmset"])
    async def lastfmset(self, ctx):
        """Instructions on how to set the api key."""
        message = (
            "1. Vist the [LastFM](https://www.last.fm/api/) site and click on 'Get an API Account'.\n"
            "2. Fill in the application. Once completed do not exit the page. - "
            "Copy all information on the page and save it.\n"
            f"3. Enter the key via `{ctx.clean_prefix}set api lastfm appid <appid_here>`"
        )
        await ctx.maybe_send_embed(message)

    @commands.check(tokencheck)
    @commands.group(case_insensitive=True)
    async def fm(self, ctx):
        """Last.fm commands"""

    @fm.command()
    async def set(self, ctx, username):
        """Save your last.fm username."""
        try:
            content = await self.get_userinfo_embed(ctx, username)
        except LastFMError as e:
            return await ctx.send(str(e))
        if content is None:
            return await ctx.send(f"\N{WARNING SIGN} Invalid Last.fm username `{username}`")

        await self.config.user(ctx.author).lastfm_username.set(username)
        await ctx.send(
            f"{ctx.message.author.mention} Username saved as `{username}`", embed=content,
        )

    @fm.command()
    async def unset(self, ctx):
        """Unlink your last.fm."""
        await self.config.user(ctx.author).lastfm_username.set(None)
        await ctx.send("\N{BROKEN HEART} Removed your last.fm username from the database")
        async with self.config.guild(ctx.guild).crowns() as crowns:
            crownlist = []
            for crown in crowns:
                if crowns[crown]["user"] == ctx.author.id:
                    crownlist.append(crown)
            for crown in crownlist:
                del crowns[crown]

    @fm.command()
    async def profile(self, ctx, user: Optional[discord.Member] = None):
        """Lastfm profile."""
        author = user or ctx.author
        name = await self.config.user(author).lastfm_username()
        if name is None:
            return await ctx.send(
                "You do not have a LastFM account set. Please set one with {}fm set".format(
                    ctx.clean_prefix
                )
            )
        try:
            await ctx.send(embed=await self.get_userinfo_embed(ctx, name))
        except LastFMError as e:
            return await ctx.send(str(e))


    @commands.command(aliases=["lyr"])
    async def lyrics(self, ctx, *, track: str = None):
        """Currently playing song or most recent song."""
        #player = lavalink.get_player(ctx.guild.id)
        #track = re.sub(r'\s+','-', ' ', track).strip()
        if track is None:
            name = await self.config.user(ctx.author).lastfm_username()
            if name is None:
                name = await self.config.user(ctx.author).lastfm_username()
                #return await ctx.send(
                    #"You do not have a LastFM account set. Please set one with `{}fm set`.".format(
                        #ctx.clean_prefix
                    #)
                #)
            try:
                data = await self.api_request(
                    ctx, {"user": name, "method": "user.getrecenttracks", "limit": 1}
                )
            except LastFMError as e:
                return await ctx.send(str(e))
            tracks = data["recenttracks"]["track"]

            if not tracks:
                embed = discord.Embed(colour= (await ctx.embed_colour()), title="You must specify a song name!")
                #return await ctx.send(track)
                return await ctx.send(embed=embed)
                #return await ctx.send("You have not listened to anything yet!")

            artist = tracks[0]["artist"]["#text"]
            track = tracks[0]["name"]
            image_url = tracks[0]["image"][-1]["#text"]
            # image_url_small = tracks[0]['image'][1]['#text']
            # image_colour = await color_from_image_url(image_url_small)

            # content = discord.Embed(color=await self.bot.get_embed_color(ctx.channel))
            # content.colour = int(image_colour, 16)
            title = (
                f"**{escape(artist, formatting=True)}** — ***{escape(track, formatting=True)} ***"
            )

            # tags and playcount
            if "@attr" in tracks[0]:
                if "nowplaying" in tracks[0]["@attr"]:
                    results, songtitle = await self.lyrics_musixmatch(f"{artist} {track}")
                    if results is None:
                        return await ctx.send(f'No lyrics for "{artist} {track}" found.')
                    embeds = []
                    results = list(pagify(results, page_length=2048))
                    for i, page in enumerate(results, 1):
                        content = discord.Embed(
                            color=await self.bot.get_embed_color(ctx.channel),
                            description=page,
                            title=title,
                        )
                        content.set_thumbnail(url=image_url)
                        content.set_footer(text=f"Page {i}/{len(results)}")

                        embeds.append(content)
                    if len(embeds) > 1:
                        await menu(ctx, embeds, DEFAULT_CONTROLS)
                    else:
                        await ctx.send(embed=embeds[0])
            else:
                await ctx.send("You're not currently playing a song.")
        else:
            # content.colour = int(image_colour, 16)

            results, songtitle = await self.lyrics_musixmatch(track)
            if results is None:
                return await ctx.send(f'No lyrics for "{track}" found.')
            embeds = []
            results = list(pagify(results, page_length=2048))
            for i, page in enumerate(results, 1):
                content = discord.Embed(
                    color=await self.bot.get_embed_color(ctx.channel),
                    title=f"***{escape(songtitle, formatting=True)} ***",
                    description=page,
                )
                content.set_footer(text=f"Page {i}/{len(results)}")
                embeds.append(content)
            if len(embeds) > 1:
                await menu(ctx, embeds, DEFAULT_CONTROLS)
            else:
                await ctx.send(embed=embeds[0])

