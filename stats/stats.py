import datetime
import os
import discord
from random import randint
from redbot.core import checks, commands
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
import lavalink
import asyncio
import re
import subprocess
from collections import Counter
try:
    import psutil

    psutilAvailable = True
except ImportError:
    psutilAvailable = False

try:
    import speedtest
    module_avail = True
except ImportError:
    module_avail = False

from redbot.core import (
    __version__,
    version_info as red_version_info,
)


class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ctx.bot.user.name
    # if ctx.invoked_subcommand is None:
    #       await ctx.send_help()

    def speed_test(self):
        return str(subprocess.check_output(['speedtest-cli'], stderr=subprocess.STDOUT))
    
    @commands.command(aliases=["statistics"], pass_context=True)
    async def stats(self, ctx):
        """Statistics!"""

        await ctx.message.add_reaction('\u2699')

        #waiting = await ctx.send("Gathering information...")

        name = ctx.bot.user.name
        users = str(len(set(ctx.bot.get_all_members())))
        servers = str(len(ctx.bot.guilds))
        channels = str(len(set(ctx.bot.get_all_channels())))
        #try:
            #DOWNLOAD_RE = re.compile(r"Download: ([\d.]+) .bit")
            #UPLOAD_RE = re.compile(r"Upload: ([\d.]+) .bit")
            #PING_RE = re.compile(r"([\d.]+) ms")
            #speedtest_result = await self.bot.loop.run_in_executor(None, self.speed_test)
            #download = float(DOWNLOAD_RE.search(speedtest_result).group(1))
            #upload = float(UPLOAD_RE.search(speedtest_result).group(1))
            #ping = float(PING_RE.search(speedtest_result).group(1))
        #except KeyError:
            #print("An error occured")

        process = psutil.Process()
        cpu_usage = psutil.cpu_percent()

        boot_s = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%d-%m-%y %H:%M:%S")

        disk_u = psutil.disk_usage(os.path.sep)
        disk = disk_u.percent

        mem_v = psutil.virtual_memory()
        memoryused = self._size(mem_v.total - mem_v.available)
        memorytotal = self._size(mem_v.total)
        memorypercent = mem_v.percent

        net_io = psutil.net_io_counters()
        bytes_recv = self._size(net_io.bytes_recv)
        bytes_sent = self._size(net_io.bytes_sent)

        since = ctx.bot.uptime.strftime("%d-%m-%y at %H:%M:%S")

        #commands_run = ctx.bot.counter['processed_commands']
        #read_messages = ctx.bot.counter['messages_read']
        #commands_run = "N/A"
        #read_messages = "N/A"

        #listening = len([p for p in lavalink.players if p.current is not None])
        
        connections = len(lavalink.all_players())
        if connections == 0:
            connections =  "No connections."
        else:
            connections = len(lavalink.all_players())

        if self.bot.get_cog("Audio")== None:
            lavastatus = "<:dndicon:482526601884467211>Offline"
        else:
            lavastatus = "<:onlineicon:482511784968716288>Online"

        latencies = self.bot.latencies
        shardmsg = ""
        pingmsg = ""
        for shard, pingt in latencies:
            shardmsg += "{}/{}".format(shard + 1, len(latencies))
            pingmsg += "{}ms\n".format(round(pingt*1000))
        
        dpy_version = discord.__version__
        redver = red_version_info
        #botowner = ctx.bot.owner_ids
        botowner = "Nexus Hub"

        em = discord.Embed(title=name + " (Version {})".format(redver), description= "NexusBot is a simple and easy to use custom Discord music bot offering high quality Music. Server information commands and more!", colour=(await ctx.embed_colour()))
        em.set_thumbnail(url=ctx.bot.user.avatar_url)
        em.add_field(name="Developers", value=botowner, inline=False)
        em.add_field(name="Discord.py", value="[{}](https://github.com/Rapptz/discord.py)".format(dpy_version))
        em.add_field(name="Version", value="{}-NexusBotV3".format(redver))
        em.add_field(name="Channels", value="{}".format(channels))
        em.add_field(name="Users", value="{}".format(users))
        em.add_field(name="Guilds", value="{}".format(servers))
        #em.add_field(name="Commands ran", value=commands_run)
        #em.add_field(name="Messages received", value=read_messages)
        #em.add_field(name="CPU", value="{}%".format(cpu_usage))
        #em.add_field(name="Memory", value="{} / {}".format(memoryused, memorytotal))
        #em.add_field(name='Network', value='Sent: {}\n Received: {}'.format(bytes_sent, bytes_recv))
        #em.add_field(name="Ping", value=pingmsg)
        em.add_field(name='Streams', value=connections)
        em.add_field(name='Uptime', value='{}\n'.format(self.get_bot_uptime(brief=True)))
        em.set_footer(text="Page 1/2 | Shard {} | Last restarted: {}".format(shardmsg, since))

        info = "Here is some information and links for the bot."
        page2 = discord.Embed(title="System Information", description= "NexusBot is a simple and easy to use custom Discord music bot offering high quality Music. Server information commands and more!", colour=(await ctx.embed_colour()))
        page2.set_thumbnail(url=ctx.bot.user.avatar_url)
        #page4.set_thumbnail(url=ctx.bot.avatar_url)
        #page2.add_field(name="Owner", value="<@{}>".format(ctx.bot.owner_id))
        page2.add_field(name='Lavalink status', value=lavastatus, inline=False)
        page2.add_field(name="Boot time", value="{}".format(boot_s))
        page2.add_field(name="CPU", value="{}%".format(cpu_usage))
        page2.add_field(name="Memory", value="{} [{}%]".format(memoryused, memorypercent))
        page2.add_field(name="Disk usage", value="{}%".format(disk))
        page2.add_field(name='Network traffic', value='Sent: {}\nReceived: {}'.format(bytes_sent, bytes_recv))
        page2.add_field(name="Ping", value=pingmsg)
        #page2.add_field(name='Network speed', value='Download **{}** mbps\nUpload **{}** mbps\n Latency **{}** ms'.format(download, upload, ping))
        page2.set_footer(text="Page 2/2 | Shard {} | Last restarted: {}".format(shardmsg, since))
        embeds = [em, page2]

        #await waiting.delete()
        await menu(ctx, embeds, DEFAULT_CONTROLS)
        #await ctx.send(embed=em)
        

    @staticmethod
    def _size(num):
        for unit in ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]:
            if abs(num) < 1024.0:
                return "{0:.1f}{1}".format(num, unit)
            num /= 1024.0
        return "{0:.1f}{1}".format(num, "YB")
    
    def get_bot_uptime(self, *, brief=False):
        # Stolen from owner.py - Courtesy of Danny
        now = datetime.datetime.utcnow()
        delta = now - self.bot.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if not brief:
            if days:
                fmt = '{d}d {h}h {m}m {s}s'
            else:
                fmt = '{h}h {m}m {s}s'
        else:
            fmt = '{h}h {m}m {s}s'
            if days:
                fmt = '{d}d ' + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)
    
    @commands.command(aliases=["guinfo"], pass_context=True)
    async def globaluserinfo(self, ctx, id: str):
        """Gives you the info of ANY user."""

        if not ctx.bot.user.bot:
            await ctx.send("``This is not a bot account\n"
                               "It only works with bot accounts")
            return

        if not id.isdigit():
            await ctx.send("You can only use IDs from a user!")
            return

        try:
            user = await ctx.bot.get_user_info(id)
        except discord.errors.NotFound:
            await ctx.send("No user with the id `{}` found.".format(id))
            return
        except:
            await ctx.send("An error has occured.")
            return

        colour = (await ctx.embed_colour())

        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        since_created = (ctx.message.created_at - user.created_at).days

        created_on = "{}\n({} days ago)".format(user_created, since_created)

        if user .avatar_url.find("gif") != -1:
            nitro = True
        else:
            nitro = False

        if user.bot == False:
            data = discord.Embed(description="User ID : " +
                                 str(user.id), colour=colour)
        else:
            data = discord.Embed(
                description="**BOT** | User ID : " + str(user.id), colour=colour)

        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Nitro", value=nitro)

        if user.avatar_url:
            data.set_author(name="{}#{}".format(
                user.name, user.discriminator), url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name="{}#{}".format(
                user.name, user.discriminator), url=user.default_avatar_url)
            data.set_thumbnail(url=user.default_avatar_url)

        try:
            await ctx.send(embed=data)
        except:
            await ctx.send("I need the `Embed links` permission "
                               "to send this")