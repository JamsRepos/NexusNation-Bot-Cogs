import discord, datetime, asyncio, aiohttp, decimal
from redbot.core import commands, checks, Config
import discord.ext.tasks
import lavalink
from redbot.core.utils.chat_formatting import bold, humanize_number, humanize_timedelta, pagify

import mysql.connector
from mysql.connector import Error
from .sql_connect import connect

async def get_channels(client):
    count = 0
    try:
        for i in client.guilds:
            count += len(i.text_channels)
            count += len(i.voice_channels)
        return count
    except Exception as e:
        print(e)

class StatsMain(commands.Cog):

    __author__ = "Created by Raff, fucked by Bramble"
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.update_db.start()

    def cog_unload(self):
        self.update_db.cancel()
    
    @discord.ext.tasks.loop(minutes=1.0)
    async def update_db(self):
        # this has to be nested in here or has issues grabbing self from Red.
        if self.bot.get_cog("Audio") == None:
            connections = 0
        else:
            connections = len(lavalink.all_players())

        guilds = len(self.bot.guilds)
        users = len(self.bot.users)
        commands = len(self.bot.commands)
        channels = await get_channels(self.bot)
        connect('nexusbot', f"UPDATE `bot_stats` SET `servers` = {guilds}, `users` = {users}, `channels` = {channels}, `commands` = {commands}, `streams` = {connections} WHERE ID = 1")
