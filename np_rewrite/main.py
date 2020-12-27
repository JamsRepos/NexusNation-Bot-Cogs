import discord
import lavalink
from discord.ext import commands as dpy_commands
from redbot.core import commands
from redbot.core.utils.menus import DEFAULT_CONTROLS, close_menu, menu

from .handles import format_time, draw_time, control_list
from .menu import skip_current, pause_current, stop_current, prev_current, shuffle, repeat, queue, controls

class PinguNow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("now")

    @commands.command()
    async def now(self, ctx: commands.Context):
        """Now playing song"""
        try:
            player = lavalink.get_player(ctx.guild.id)
        except KeyError:
            error = discord.Embed(
                title=f"Nothing playing in {ctx.guild.name}!",
                colour=(await ctx.embed_colour())
                )
            return await ctx.send(embed=error)
        
        pos = await format_time(player.position)

        requester = ("<@{track.requester.id}>").format(track=player.current)
        arrow = await draw_time(ctx)
        controllers = await control_list(ctx)
        paused = player.paused
        if paused:
            paused_state = "\N{DOUBLE VERTICAL BAR}\N{VARIATION SELECTOR-16}"
            song_state = "Paused"
        else:
            paused_state = "\N{BLACK RIGHT-POINTING TRIANGLE}\N{VARIATION SELECTOR-16}"
            song_state = "Now Playing"
        
        if player.current.is_stream:
            dur = "LIVE"
            song_state = "Streaming LIVE 🔴"
        else:
            dur = await format_time(player.current.length)

        current = discord.Embed(
            colour=(await ctx.embed_colour()))
        current.set_author(
            name=f"Now Playing in {ctx.guild.name}",
            icon_url="https://pingubot.fun/img/track.gif"),
            
        current.add_field(
            name=f"{paused_state} {song_state}",
            value=f"[{player.current.title}]({player.current.uri})",
            inline=False)
        current.add_field(name="Duration", value=f"`{pos}` / `{dur}`")
        current.add_field(name="Requester", value=requester)
        current.add_field(name="Progress", value=arrow, inline=False)
        current.add_field(name="Controls", value=controllers, inline=False)
        current.set_thumbnail(url=player.current.thumbnail)

        pages = [current]
        await menu(ctx, pages, controls)