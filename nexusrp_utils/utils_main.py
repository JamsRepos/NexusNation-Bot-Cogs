import discord, datetime, asyncio, aiohttp
from redbot.core import commands, checks, Config

class nexusUtils(commands.Cog):

    __author__ = "Raff"
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        # Setup variables
        discord_server = discord.utils.get(self.bot.guilds, id=699702073951912028)
        bot_commands_channel = discord.utils.get(discord_server.text_channels, id=713173661523116043)
        #
        

        # Nexus RP instagram reaction adder

        if (message.channel.id = 713173512533311528):
            if (":ig:" not in message.content):
                await message.delete()
                try:
                    message.author.send("Please format your instagram posts properly by including the `:ig:` emoji")
                except discord.errors.Forbidden:
                    bot_commands_channel.send(f"{message.author.mention} Please format your instagram posts properly by including the :ig: emoji")
            if (len(message.attachments)>0):
                message.add_reaction("❤️")
        else: 
            pass

        #
        