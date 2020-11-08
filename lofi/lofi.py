import discord
import lavalink
from redbot.core import commands
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu, close_menu
from discord.ext import commands as dpy_commands
from typing import Union


class Lofi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def lofi(self, ctx):

        lofi_links = """
            `1.` Lofi LIVE
            `2.` Lofi Hip Hop
            `3.` Lofi Popular 2020
            `4.` Lofi 2AM
            """
        query_one = "https://www.youtube.com/watch?v=5qap5aO4i9A"
        query_two = "https://www.youtube.com/watch?v=WTsmIbNku5g&list=PLOzDu-MXXLliO9fBNZOQTBDddoA3FzZUo"
        query_three = "https://www.youtube.com/watch?v=1WGCADztYKs"
        query_four = "https://www.youtube.com/watch?v=EJew8Mvgau0"

        em = discord.Embed(title="Lofi playlists:",
        description=lofi_links, colour=(await ctx.embed_colour()))

        async def one(ctx, pages, controls, message: discord.Message, page, timeout, emoji,):

            if message:
                getplay = self.bot.get_command("play")
                output = await ctx.invoke(getplay, query=query_one)
                await message.delete()
                return output

        async def two(ctx, pages, controls, message: discord.Message, page, timeout, emoji,):

            if message:
                getplay = self.bot.get_command("play")
                output = await ctx.invoke(getplay, query=query_two)
                await message.delete()
                return output

        async def three(ctx, pages, controls, message: discord.Message, page, timeout, emoji,):

            if message:
                getplay = self.bot.get_command("play")
                output = await ctx.invoke(getplay, query=query_three)
                await message.delete()
                return output

        async def four(ctx, pages, controls, message: discord.Message, page, timeout, emoji,):

            if message:
                getplay = self.bot.get_command("play")
                output = await ctx.invoke(getplay, query=query_four)
                await message.delete()
                return output

        controls = {
            "\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}": one,
            "\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}": two,
            "\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}": three,
            "\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}": four,
            "\N{CROSS MARK}": close_menu,
        }

        pages = [em]

        # run the actual menu
        await menu(ctx, pages, controls)