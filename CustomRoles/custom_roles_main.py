import aiohttp, asyncio, discord, datetime, time, json

from redbot.core import commands
from redbot.core import checks, Config
from discord.ext import tasks


def role_check():
    async def checker(ctx):
        '''
        if ctx.author in ctx.guild.premium_subscribers:
            return True
        '''
        allowed = [585551637855076364]
        for role in allowed:
            check_role = discord.utils.get(ctx.guild.roles, id=role)
            if check_role in ctx.author.roles:
                return True
    return commands.check(checker)


class CustomRoles(commands.Cog):

    __author__ = "Raff"
    __version__ = "1.0.0"
    ...
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2227456312)
        default_guild = {
            "custom_roles": [],
            #role names you don't want users to be able to use can be put here. you can also use !disallowrolename <name> to add to the disallowed role names list
            "disallowed_role_names": [
                "admin",
                "administrator",
                "owner",
                "coowner",
                "co-owner",
                "co owner",
                "retired owner",
                "retiredowner"
                "manager",
                "management",
                "manager",
                "moderator",
                "temp moderator",
                "temp mod",
                "tempmod",
                "tempmoderator",
                "head admin",
                "headadmin",
                "serverop",
                "server operator",
                "serveroperator",
                "vip",
                "vip+",
                "nitro booster",
                "nitrobooster",
                "contentcreator",
                "content creator",
                "top donator",
                "official bot"
                ]
        }
        default_member = {
            "role_id": 0,
            "has_role": False
        }
        self.config.register_guild(**default_guild)
        self.config.register_member(**default_member)
    ...
    @commands.command(name="role")
    @role_check()
    async def set_custom_role(self, ctx, role_colour: str = "ffffff", *, role_name: str = "MyCustomRole"):
        if role_name.lower() not in await self.config.guild(ctx.guild).disallowed_role_names() and len(role_name.lower()) <= 32:
            deleterole=False
            try:
                if await self.config.member(ctx.author).has_role():
                    roleid = await self.config.member(ctx.author).role_id()
                    role_deletion = discord.utils.get(ctx.guild.roles, id=int(roleid))
                    deleterole=True

                if "#" in role_colour:
                    role_colour = role_colour.replace("#", "")

                col = discord.Color(value=int(role_colour, 16))
                col = col.to_rgb()

                new_role = await ctx.guild.create_role(name=f"{role_name}", color=discord.Color.from_rgb(*col))

                await ctx.author.add_roles(new_role, reason=f"Custom Nitro Booster role - created by {ctx.author.name}")

                await ctx.send(f"Role {new_role.mention} created!")

                await self.config.member(ctx.author).role_id.set(new_role.id)
                await self.config.member(ctx.author).has_role.set(True)
                async with self.config.guild(ctx.guild).custom_roles() as customs:
                    customs.append(new_role.id)
                    await asyncio.sleep(1)
                    for role in customs:
                        try:
                            c_role = discord.utils.get(ctx.guild.roles, id=int(role))
                            if c_role != None:
                                above_role = discord.utils.get(
                                    ctx.guild.roles, id=700509065025159228)
                                await c_role.edit(position=(above_role.position-1))
                            else:
                                pass
                        except Exception as e:
                            print(e)

                if deleterole:
                    await role_deletion.delete()
                    async with self.config.guild(ctx.guild).custom_roles() as customs:
                        if role_deletion.id in customs:
                            customs.remove(role_deletion.id)
                        else:
                            pass

            except ValueError:
                await ctx.send("Please enter a valid Hex code.")
        else:
            await ctx.send("You cannot create a role with that name.")
    ...
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def disallowrolename(self, ctx, *, role_name:str):
        async with self.config.guild(ctx.guild).disallowed_role_names() as roles:
            roles.append(role_name.lower())
        await ctx.send(f"Added **{role_name}** to the disallowed custom role names list")
    ...
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def allowrolename(self, ctx, *, role_name: str):
        async with self.config.guild(ctx.guild).disallowed_role_names() as roles:
            if role_name.lower() in roles:
                roles.remove(role_name.lower())
                await ctx.send(f"Removed **{role_name.lower()}** from the disallowed custom role names list")
            else:
                await ctx.send(f"**{role_name.lower()}** is not in the disallowed custom role names list")
    ...
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removememberrole(self, ctx, member: discord.Member, *, reason: str = "No reason given"):
        try:
            if await self.config.member(member).has_role():
                role = await self.config.member(member).role_id()
                role_to_remove = discord.utils.get(ctx.guild.roles, id=role)
                await ctx.send(f"I have deleted the custom role **{role_to_remove.name}** from **{ctx.guild.name}'s** roles.")
                async with self.config.guild(ctx.guild).custom_roles() as customs:
                    if role_to_remove.id in customs:
                        customs.remove(role_to_remove.id)
                await member.send(f"Your custom role **{role_to_remove.name}** has been removed.\nReason: {reason}")
                await role_to_remove.delete()
                await self.config.member(member).role_id.set(0)
                await self.config.member(member).has_role.set(False)

            else:
                await ctx.send(f"**{member.name}** does not have a custom role")
        except Exception as e:
            print(e)
    ...
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        booster_role = discord.utils.get(
            after.guild.roles, id=585551637855076364)
        try:
            if booster_role in before.roles and booster_role not in after.roles:
                if self.config.member(after).has_role:
                    role = discord.utils.get(after.guild.roles, id=(await self.config.member(after).role_id()))
                    await after.send(f"You are no longer boosting our guild, therefore your custom role \"{role.name}\" has been removed.")
                    async with self.config.guild(after.guild).custom_roles() as customs:
                        if role.id in customs:
                            customs.remove(role.id)
                    await role.delete()
                    await self.config.member(after).role_id.set(0)
                    await self.config.member(after).has_role.set(False)
                else:
                    pass
            else:
                pass
        except Exception as e:
            print(e)
    ...
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.config.member(member).has_role:
            role_to_remove = discord.utils.get(member.guild.roles, id = (await self.config.member(member).role_id()))
            await self.config.member(member).has_role.set(False)
            await self.config.member(member).role_id.set(0)
            async with self.config.guild(member.guild).custom_roles() as customs:
                if role_to_remove != None:
                    if role_to_remove.id in customs:
                        customs.remove(role_to_remove.id)
                    await role_to_remove.delete()

