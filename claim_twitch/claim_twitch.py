import aiohttp
import asyncio
import discord
import datetime
import time
import json
from redbot.core import commands
from redbot.core import checks, Config
from discord.ext import tasks

from .sql_connect import read, write

def communityid_converter(communityid):
    steamid64ident = 76561197960265728
    sid_split = communityid.split(':')
    commid = int(sid_split[2]) * 2
    if sid_split[1] == '1':
        commid += 1
    commid += steamid64ident
    return commid

def ifconfig():
    async def predicate(ctx):
        cog = ctx.cog
        url = await cog.config.guild(ctx.guild).url()
        api_key = await cog.config.guild(ctx.guild).api_key()
        if not (url and api_key):
            raise commands.UserFeedbackCheckFailure(message="You need to setup Prometheus server url and api key first!")
        else:
            return True
    return commands.check(predicate)

def is_sub():
    async def predicate(ctx):
        rolename = await ctx.cog.config.guild(ctx.guild).role_name()
        for x in ctx.author.roles:
            if x.name == rolename:
                return True
        raise commands.UserFeedbackCheckFailure(message="You are not currently subscribed to <https://twitch.tv/LubricantJam>. Please click the link and find the **Subscribe Free** button. \nIf you do not see this, you do not have **Twitch Prime** linked to your account. You can link by following this link <https://gaming.amazon.com/>.")
    return commands.check(predicate)

class Claim_Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=8797456312)
        default_guild = {
            "package": 0,
            "couldown": 31, ##cooldown is in days, cuz it's easier
            "role_name": "Jam's Twitch Sub"
        }
        default_member = {
            "last_claim": 0,
            "steamid": 0,
            "remind": False
        }
        self.config.register_guild(**default_guild)
        self.config.register_member(**default_member)
        self.time_then = 0
        self.bot_commands_channel_id = 269933786853015553 # Bot commands channel ID
        self.role_id = 761683196365766686
        self.guild_id = 269912749327253504 # Guild ID
        self.twitch_channel_id = 664889221579931658 # New Sub Channel ID
        self.claimReminder.start()

    def cog_unload(self):
        self.claimReminder.cancel()

    @commands.group()
    @checks.admin()
    async def claimset_twitch(self, ctx):
        """Main group for setting up the cog."""
        pass

    @claimset_twitch.command()
    @checks.admin()
    async def url(self, ctx, url):
        """Set the url of your Prometheus server.
        Note that you need to point it to api.php."""
        await self.config.guild(ctx.guild).url.set(url)
        await ctx.send(f"Prometheus url set to {url}")

    @claimset_twitch.command()
    @checks.admin()
    async def apikey(self, ctx, apikey):
        """Set the api key for the Prometheus server.
        Better use that in a private channel, as it won't work on DMs.
        Note that command will autodelete itself to prevent api key leak."""
        try:
            await ctx.delete()
        except:
            pass
        await self.config.guild(ctx.guild).api_key.set(apikey)
        await ctx.send("Successfully saved the api key.")

    @claimset_twitch.command()
    @checks.admin()
    async def package(self, ctx, package:int=0):
        """Set the package ID for the package redeemed.
        Defaults to 0"""
        await self.config.guild(ctx.guild).package.set(package)
        await ctx.send(f"Successfully saved {package} package to be given on claim.")

    @claimset_twitch.command()
    @checks.admin()
    async def cooldown(self, ctx, cooldown:int=31):
        """Set the cooldown between 2 claims (in days).
        Defaults to 31 days."""
        await self.config.guild(ctx.guild).cooldown.set(cooldown)
        await ctx.send(f"Successfully set claim cooldown to {cooldown} days.")

    @claimset_twitch.command()
    @checks.admin()
    async def role(self, ctx, role : discord.Role):
        """If you changed Twitch Subscriber role's name, and everything's broken, use this command tagging the role to fix everything."""
        await self.config.guild(ctx.guild).role_name(role.name)
        await ctx.send("Successfully saved the role.")

    @ifconfig()
    @is_sub()
    @commands.command()
    async def claimvip(self, ctx):
        """Claim your monthly tokens as a Twitch Subscriber."""
        userid = read('discord_integration', f"SELECT IFNULL( (SELECT steamid FROM `du_users` WHERE userid = {str(ctx.author.id)}) , 0);")
        await self.config.member(ctx.author).steamid.set(userid)

        store = read('store', f"SELECT IFNULL( (SELECT id FROM `players` WHERE uid = {userid}) , 0);")
        if store == 0:
            return await ctx.send(f"In order to claim **VIP**, please ensure you have signed in at least **ONCE** to our Donation Store.\n**Visit our Store:** https://nexushub.io/")
        
        url = await self.config.guild(ctx.guild).url()
        apikey = await self.config.guild(ctx.guild).api_key()
        package = await self.config.guild(ctx.guild).package()
        cooldown = await self.config.guild(ctx.guild).cooldown()
        lastclaim = await self.config.member(ctx.author).last_claim()
        steamid = await self.config.member(ctx.author).steamid()
        lastclaimdt = datetime.datetime.fromtimestamp(int(lastclaim))
        now = datetime.datetime.now()
        nextclaim = cooldown - (now - lastclaimdt).days
        if (now - lastclaimdt).days < int(cooldown):
            return await ctx.send(f"You have already claimed recently. You have **{nextclaim}** days left until you can claim again.")
        if steamid == 0:
            return await ctx.send("You have not linked your Steam account to perform this command.")
        req = f"?hash={apikey}&steamid={steamid}&action=assignPackage&package={package}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url + req) as resp:
                json = await resp.json()
                if not str(steamid).isdigit():
                    await ctx.send(f"You have attempted to use **{steamid}** as your **User ID**. Please change this before attempting again.")
                elif json["error"]:
                    return await ctx.send(f"An error occured:\n{json['error']}")
                else:
                    await ctx.send(f"You have successfully redeemed **VIP**. Thank you for supporting our servers.")
                    await self.config.member(ctx.author).last_claim.set(int(time.time()))


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        twitch_role = before.guild.get_role(self.role_id)
        if twitch_role != None:
            current_twitch = twitch_role in before.roles
        else:
            current_twitch = False

        if twitch_role in after.roles and not current_twitch:
            channel_obj = self.bot.get_channel(self.twitch_channel_id)
            if channel_obj != None:
                await channel_obj.send("Thanks for subscribing to <https://twitch.tv/LubricantJam/> {}, you can now obtain free VIP by typing ``!claimvip`` in <#269933786853015553>.\nIf you would like to be notified when you can claim again, please use ``!vipreminder`` in <#269933786853015553>.".format(after.mention))

    @tasks.loop(minutes=15)
    async def claimReminder(self):
        has_role = False
        channel = self.bot.get_channel(self.bot_commands_channel_id) #channel id to send messages in
        timenow = int(time.time())

        if self.time_then <= (timenow-43200):
            
            for member in self.bot.get_guild(int(self.guild_id)).members:
                lastclaim = await self.config.member(self.bot.get_guild(self.guild_id).get_member(member.id)).last_claim()
                for r in self.bot.get_guild(self.guild_id).get_member(member.id).roles:
                    if r.id == self.role_id:
                        has_role = True
                        break
                    elif r.id != self.role_id:
                        has_role = False
                if (has_role == True) and (lastclaim <= (timenow-2592000)) and (await self.config.member(self.bot.get_guild(self.guild_id).get_member(member.id)).remind() == True):
                    discord_member_id = '<@!'+str(member.id)+'>'
                    await channel.send(discord_member_id + ", You can now claim free VIP, type `!claimvip` in <#269933786853015553>. This reminder will stop once you claim your reward or use ``!vipreminder`` to toggle this alert.") 
                    has_role = False
                else:
                    pass
            previous_announcement = (int(timenow)-int(self.time_then))
            print("Time since last announcement: {} minutes - should be: {}".format(int(int(previous_announcement)/60), 720))
            print("Announced at {}".format(timenow))
            self.time_then = int(time.time())
            print("Waiting {} minutes till next announcement".format(int(43200/60)))
                    

    @claimReminder.before_loop
    async def before_claimReminder(self):
        await self.bot.wait_until_ready()

        now = datetime.datetime.now()
        seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        print(int(seconds_since_midnight))
        if int(seconds_since_midnight) >= 32400 and int(seconds_since_midnight) <= 75600 : # if seconds since midnight is more than 9am
            time_to_wait = (75600-int(seconds_since_midnight))
        elif int(seconds_since_midnight) >= 75600: # if seconds since midnight is more than 9pm
            time_to_wait = (((86400+32400)-int(seconds_since_midnight)))
        elif int(seconds_since_midnight) <= 32400: # if seconds since midnight is less than 9am
            time_to_wait = (32400 - int(seconds_since_midnight))
        print("Waiting {} seconds to run the claim reminder loop".format(int(time_to_wait)))
        await asyncio.sleep(
            int(time_to_wait)
            )  # time to wait until loop starts


    @commands.command()
    @is_sub()
    async def vipreminder(self, ctx):
        if await self.config.member(ctx.author).remind():
            await self.config.member(ctx.author).remind.set(False)
            await ctx.send(f"{ctx.author.mention} You will **no longer** be notified when you can use ``!claimvip`` again.")
        elif not await self.config.member(ctx.author).remind():
            await self.config.member(ctx.author).remind.set(True)
            await ctx.send(f"{ctx.author.mention} You will **now** be notified when you can use ``!claimvip`` again.")
