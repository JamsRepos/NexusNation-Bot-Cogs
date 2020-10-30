import discord, datetime, asyncio, aiohttp, decimal
from redbot.core import commands, checks, Config
from redbot.core.utils.chat_formatting import humanize_number, humanize_timedelta,

from .sqlconnect import connect
from databases import Database
import discord.ext.tasks


class DiscordMembers(commands.Cog):


    __author__ = "Venom"
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot


    @discord.ext.tasks.loop(minutes=1.0)
    async def update_db(self):
        guilds = ['269912749327253504', '759037208341774367']
        for guild_id in guilds:
            guild = bot.get_guild(guild_id)
            total_guild_members = (str(len(guild.members)))
            VALUES = [
                {"guild": guild_id, "count": total_guild_members,
            ]
            connect("INSERT INTO discord_members (guild, count) VALUES(:guild, :count) ON DUPLICATE KEY UPDATE count = :count;" )

