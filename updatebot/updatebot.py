import asyncio
import subprocess
import sys
import threading
from asyncio.subprocess import PIPE
from subprocess import Popen

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import format_perms_list, pagify


class UpdateBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def updatebot(self, ctx):
        """Attempt to update bot version"""
        await ctx.send("Attempting update bot. Restart the bot after.")
        proc = await asyncio.create_subprocess_shell('"{python}" -m pip install -U Red-DiscordBot'.format(python=sys.executable), 
                                                     stdin=None, stderr=None, stdout=PIPE)
        out = await proc.stdout.read()
        msg = pagify(out.decode('utf-8'))
        
        for page in msg:
            await ctx.send("```py\n\n{}```".format(page))
