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

async def get_streams(client):
    connections = len(lavalink.all_players())
    if connections == 0:
        connections = "0"
    else:
        connections = len(lavalink.all_players())
        return connections

class StatsMain(commands.Cog):

    __author__ = "Raff"
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.update_db.start()

    def cog_unload(self):
        self.update_db.cancel()
    
    @discord.ext.tasks.loop(minutes=5.0)
    async def update_db(self):
        guilds = len(self.bot.guilds)
        users = len(self.bot.users)
        commands = len(self.bot.commands)
        channels = await get_channels(self.bot)
        streams = await get_streams(self.bot)
        connect('cicada_discordbot', f"UPDATE `bot_stats` SET `servers` = {guilds}, `users` = {users}, `channels` = {channels}, `commands` ={commands}, `streams` = {streams} WHERE ID = 1")

        