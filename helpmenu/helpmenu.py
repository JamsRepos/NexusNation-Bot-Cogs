import datetime
import os
import discord
from redbot.core import checks, commands
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
import lavalink
from redbot.core.utils.chat_formatting import pagify


try:
    import psutil

    psutilAvailable = True
except ImportError:
    psutilAvailable = False


class HelpMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")
        # self.bot.remove_command("info")

    # ctx.bot.user.name
    # if ctx.invoked_subcommand is None:
    #       await ctx.send_help()

    @commands.command(hidden=True)
    @commands.guild_only()
    async def testing(self, ctx, *, commandname: str = None):
        Test = None
        if commandname is not None:
            await ctx.bot.send_help_for(ctx, commandname)
        if commandname == "all":
            await ctx.bot.send_help_for(ctx, Test)
        else:
            await ctx.send("MENU")

    @commands.command(hidden=True)
    # @commands.guild_only()
    async def help(self, ctx, *, command=None):
        prefix_string = ctx.prefix
        dpy_version = discord.__version__
        brambleid = "<@167990165258633216>"
        """Help is on the way"""
        desc = """Hello, I am `Nexus`!
        I am a administration, utility, music and fun bot packed with unique commands and fun features to offer!
        I was written in Python using [`Discord.py`](https://github.com/Rapptz/discord.py) ({}) on the [`Red`](https://github.com/Cog-Creators/Red-DiscordBot) framework.
        If you want to invite me to your guild, click [`here`](https://discordapp.com/oauth2/authorize?client_id=409819492655562767&scope=bot&permissions=8) or use `{}invite`!
        
        Here you will find pages of my different sections and the commands in them.""".format(dpy_version, prefix_string)

        since = ctx.bot.uptime.strftime("%d-%m-%y at %H:%M:%S")
        title = "Nexus Help Menu:"
        # emoji = ctx.bot.get_emoji(445640284202729472)
        author = ctx.author
        await ctx.tick()
        message = "test"
        Test = None

        connections = len(lavalink.all_players())
        if connections == 0:
            connections = "No connections."
        else:
            connections = len(lavalink.all_players())

        # PAGE 1
        page1 = discord.Embed(description=desc, colour=(await ctx.embed_colour()))
        page1.set_author(name=title, icon_url=ctx.bot.user.avatar_url)
        page1.add_field(name="Server Prefix", value="`{}`".format(prefix_string))
        page1.set_thumbnail(url=ctx.bot.user.avatar_url)
        page1.add_field(name="Streams", value=connections)
        page1.set_footer(text="Page 1/3 | Last Restart: {}".format(since))

        # PAGE 2
        generalcommands = """`ping` `avatar` `snapchat` `invite` `contact` `prefix` `stats` `userinfo` `serverinfo`"""
        moderationcommands = """`prune` `cleanup` `ban` `hackban` `ignore` `kick` `modset` `mute` `names` `rename` `slowmode` `softban` `tempban` `unban` `unignore` `unmute` `modlogsetup` `modlogset` `case` `casefor` `reason`"""
        musiccommands = """`audioset` `audiostats` `bump` `disconnect` `summon` `local` `np` `pause` `percent` `play` `playlist` `prev` `queue` `remove` `repeat` `search` `seek` `shuffle` `skip` `stop` `volume` `lyrics`"""
        nexuscommands = """`jb` `ttt` `surf` `bhop`"""
        utilitycommands = """`starboard` `customcom`  `filter` `filterset` `autorole` `alias` `google` `away` `toggleaway` `gif` `imgtfy` `imgur` `covid` `color` `autoroom` `autoroomset`"""
        page2 = discord.Embed(colour=(await ctx.embed_colour()))
        page2.set_author(name=title, icon_url=ctx.bot.user.avatar_url)
        # page2.set_thumbnail(url=ctx.bot.user.avatar_url)
        page2.add_field(
            name="Server Prefix", value="`{}`".format((prefix_string)), inline=False
        )
        page2.add_field(
            name="General Commands - 9", value=generalcommands, inline=False
        )
        page2.add_field(name="Moderation Commands - 21", value=moderationcommands, inline=False)
        page2.add_field(name="Music Commands - 25", value=musiccommands, inline=False)
        page2.add_field(name="Nexus Commands - 2", value=nexuscommands, inline=False)
        page2.add_field(
            name="Utility Commands - 15", value=utilitycommands, inline=False
        )
        page2.set_footer(text="Page 2/3 | Last Restart: {}".format(since))

        # PAGE 3
        info = "Looking for more information like statistics? Run `{}stats`.".format((prefix_string))
        page3 = discord.Embed(description=info, colour=(await ctx.embed_colour()))
        page3.set_author(name=title, icon_url=ctx.bot.user.avatar_url)
        botowner = "Nexus Hub"
        page3.add_field(name="Developers", value=botowner)
        page3.add_field(
            name="Libs",
            value="[`Discord.py`](https://github.com/Rapptz/discord.py)\n[`Red`](https://github.com/Cog-Creators/Red-DiscordBot)\n[`Lavalink.py`](https://github.com/Devoxin/Lavalink.py)",
        )
        # page4.add_field(name="Source", value="[Red-DiscordBot](https://github.com/Cog-Creators/Red-DiscordBot)")
        page3.set_footer(text=f"Page 3/3 | Last Restart: {since}")

        embeds = [page1, page2, page3]
        if command == "all":
            # await ctx.author.send(await ctx.bot.send_help_for(ctx, Test))
            await ctx.bot.send_help_for(ctx, Test)
        if command is None:
            await menu(ctx, embeds, DEFAULT_CONTROLS)
        if command is not None:
            await ctx.bot.send_help_for(ctx, command)
        return

        # await author.send("text")
        # await author.send(embed=page1)
        # await author.send(embed=page2)
        # await author.send(embed=page3)
        # await author.send(embed=page4)
