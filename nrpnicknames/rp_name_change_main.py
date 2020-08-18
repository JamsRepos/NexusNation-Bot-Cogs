import discord, datetime, asyncio, aiohttp
from redbot.core import commands, checks, Config
from discord.ext import tasks

class nameChange(commands.Cog):

    __author__ = "Raff"
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.nickname_reminder.start()

    @tasks.loop(hours=24)
    async def nickname_reminder(self):

        nexus_rp = discord.utils.get(self.bot.guilds, id=699702073951912028)
        bot_commands = discord.utils.get(nexus_rp.text_channels, id=713173661523116043)

        reminder_embed = discord.Embed(
            description="Hello and sorry for the message! I see you have not changed your nickname yet.\n\nPlease could you change your nickname to the full name of your character. If you have multiple, please seperate them with the `|` symbol.",
            color=0x2a9946,
            timestamp=datetime.datetime.utcnow()
        )
        reminder_embed.set_author(
            name="Daily Nickname Reminder",
            icon_url=nexus_rp.icon_url
        )
        reminder_embed.set_footer(
            text="Copyright © 2020 NexusHub.io"
        )
        
        for member in nexus_rp.members:
            if (member.nick is None) and not member.bot:
                try:
                    await member.send(embed=reminder_embed)
                    print(f"sent message to {member.name} reminding them to change their nickname")
                except Exception as e:
                    await bot_commands.send(content=member.mention, embed=reminder_embed)
            elif member.bot:
                print(f"{member.name} is a bot")

    @nickname_reminder.before_loop
    async def before_nickname_reminder(self):
        await self.bot.wait_until_ready()