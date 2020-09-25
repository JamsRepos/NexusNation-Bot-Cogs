import aiohttp
import asyncio
import discord
import datetime
import time
import json
from redbot.core import commands
from redbot.core import checks, Config

def guild_check():
    async def checker(ctx):
        if ctx.message.guild.id == 269912749327253504:
            return True
    return commands.check(checker)

class TopDonator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=34234234)
        default_global = {
            "donator_role": None,
            "vip_role": None,
            "vip_plus_role": None
        }
        self.config.register_global(**default_global)

    @commands.command(name="donorole")
    @guild_check()
    @commands.has_permissions(manage_roles=True)
    async def settopdonorole(self, ctx, role: discord.Role):
        await self.config.donator_role.set(role.id)
        await ctx.send(f"Top donator role set as <@&{role.id}>")

    @commands.command(name="viprole")
    @guild_check()
    @commands.has_permissions(manage_roles=True)
    async def setviprole(self, ctx, role: discord.Role):
        await self.config.vip_role.set(role.id)
        await ctx.send(f"VIP role set as <@&{role.id}>")

    @commands.command(name="vipplusrole")
    @guild_check()
    @commands.has_permissions(manage_roles=True)
    async def setvipplusrole(self, ctx, role: discord.Role):
        await self.config.vip_plus_role.set(role.id)
        await ctx.send(f"VIP+ role set as <@&{role.id}>")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if await self.config.donator_role() != None:
            top_donator_role = await self.config.donator_role()
            vip_role = await self.config.vip_role()
            vip_plus_role = await self.config.vip_plus_role()
            roles_before, roles_after = [], []
            for role in before.roles:
                roles_before.append(role.id)
            for role in after.roles:
                roles_after.append(role.id)
            if top_donator_role in roles_before\
                and top_donator_role not in roles_after:
                await after.send(f"<@!{after.id}> you are no longer a Top Donator, your donation amount has been overtaken.\n **Visit https://nexushub.io/ to re-claim your spot.**")
            elif vip_role in roles_before\
                and vip_role not in roles_after:
                await after.send(f"<@!{after.id}> you are no longer a VIP, your VIP has expired.\n **Visit https://nexushub.io/ to add more time.**")
            elif vip_plus_role in roles_before\
                    and vip_plus_role not in roles_after:
                await after.send(f"<@!{after.id}> you are no longer a VIP+, your VIP+ has expired.\n **Visit https://nexushub.io/ to add more time.**")
