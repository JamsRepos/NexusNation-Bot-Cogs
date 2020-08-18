import aiohttp, asyncio, discord, datetime, time, json

from redbot.core import commands, checks, Config
from discord.ext import tasks

def admin_check(member):
    def check_roles(member):
        roles = ['Administrator', 'Head Admin', 'Server Operator', 'Manager', 'Owner']
        for role in member.roles:
            if role.name in roles:
                return False
        return True
    return check_roles(member)
...
def authorcheck(author):
    def msg_check(message):
        if message.author == author:
            return True
        else:
            return False
    return msg_check
...
def booster_check():
    def is_booster(ctx):
        if ctx.author in ctx.guild.premium_subscribers:
            return True
    return commands.check(is_booster)
...
async def channel_getter(ctx, channeltype):
    if channeltype == "voice":
        channel_id = await ctx.cog.config.member(ctx.author).custom_voice_channel_id()
        channel = discord.utils.get(ctx.guild.channels, id = channel_id)
        return(channel)
    elif channeltype == "text":
        channel_id = await ctx.cog.config.member(ctx.author).custom_text_channel_id()
        channel = discord.utils.get(ctx.guild.channels, id=channel_id)
        return(channel)
...
async def channel_creator(ctx, overwrites, channeltype):
    if channeltype == "voice":
        category = discord.utils.get(
            ctx.guild.categories, id=(await ctx.cog.config.guild(ctx.guild).category_id()))
        ...
        if (ctx.author.name[-1]).lower() != "s":
            channel_name = f"{ctx.author.name}'s private voice channel"
        else:
            channel_name = f"{ctx.author.name} private voice channel"
        ...
        created_channel = await category.create_voice_channel(name=channel_name, overwrites=overwrites)
        ...
        await ctx.cog.config.member(ctx.author).custom_voice_channel_id.set(created_channel.id)
        await ctx.cog.config.member(ctx.author).has_voice_channel.set(True)
        async with ctx.cog.config.guild(ctx.guild).custom_voice_channels() as custom_voice_channels:
            custom_voice_channels.append(created_channel.id)
    elif channeltype == "text":
        category = discord.utils.get(
            ctx.guild.categories, id=(await ctx.cog.config.guild(ctx.guild).category_id()))
        ...
        if (ctx.author.name[-1]).lower() != "s":
            channel_name = f"{ctx.author.name}'s private text channel"
        else:
            channel_name = f"{ctx.author.name} private text channel"
        ...
        created_channel = await category.create_text_channel(name=channel_name, overwrites=overwrites)
        ...
        await ctx.cog.config.member(ctx.author).custom_text_channel_id.set(created_channel.id)
        await ctx.cog.config.member(ctx.author).has_text_channel.set(True)
        async with ctx.cog.config.guild(ctx.guild).custom_text_channels() as custom_text_channels:
            custom_text_channels.append(created_channel.id)
...
class NitroCustomChannels(commands.Cog):

    '''
    Red Discord-bot cog allowing nitro boosters to create custom, private text and voice channels
    '''

    __author__ = "Raff",
    __version__ = "1.0.0"


    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=696969)
        default_guild = {
            "category_id": 0,
            "custom_voice_channels": [],
            "custom_text_channels": [],
            "category_set": False
        }
        default_member = {
            "custom_voice_channel_id": 0,
            "has_voice_channel": False,
            "custom_text_channel_id": 0,
            "has_text_channel": False
        }
        self.config.register_guild(**default_guild)
        self.config.register_member(**default_member)
    ...
    @commands.group(name="ns")
    @commands.has_any_role('Administrator', 'Head Admin', 'Server Operator', 'Manager', 'Owner')
    async def nitro_setup(self, ctx):
        if ctx.invoked_subcommand is None:
            pass
    ...
    @nitro_setup.command()
    async def category(self, ctx):
        ...
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(
                embed_links=True,
                attach_files=True,
                use_external_emojis=True,
                add_reactions=True
                ),
        }
        if await self.config.guild(ctx.guild).category_set() == True:
            categ = await self.config.guild(ctx.guild).category_id()
            category_to_delete = discord.utils.get(ctx.guild.categories, id = categ)
            if category_to_delete != None:
                await category_to_delete.delete()
        category = await ctx.guild.create_category_channel(
            name="Custom Channels",
            overwrites=overwrites
        )
        await self.config.guild(ctx.guild).category_id.set(category.id)
        await self.config.guild(ctx.guild).category_set.set(True)
        await ctx.send(f"Created the category {category.name}. This will hold all custom channels that are created by users")
    ...
    @nitro_setup.command(description="Deletes all channels and categories related to/created by this cog",aliases=['reset'])
    async def wipe(self, ctx):
        await ctx.send("Are you sure you want to delete all channels and categories related to this cog? (yes/no)")
        sure = await self.bot.wait_for('message', check=authorcheck)
        if sure.content.lower() == "yes":
            async with self.config.guild(ctx.guild).custom_voice_channels() as custom_vc:
                for channelid in custom_vc:
                    channel = discord.utils.get(ctx.guild.channels, id = channelid)
                    if channel != None:
                        await channel.delete()
                    else:
                        pass
            async with self.config.guild(ctx.guild).custom_text_channels() as custom_txt:
                for channelid in custom_txt:
                    channel = discord.utils.get(ctx.guild.channels, id = channelid)
                    if channel != None:
                        await channel.delete()
                    else:
                        pass
            categoryid = await self.config.guild(ctx.guild).category_id()        
            category = discord.utils.get(ctx.guild.categories, id = categoryid)
            if category != None:
                await category.delete()
            else:
                pass
            await self.config.guild(ctx.guild).clear()
            await self.config.clear_all_members(guild=ctx.guild)
    ...
    @commands.group(description="Allows nitro boosters to create their own private text/voice channel",aliases=["pc", "pchannel", "privchannel"])
    @booster_check()
    async def privatechannel(self, ctx):
        if ctx.invoked_subcommand is None:
            pass
    ...
    @privatechannel.command(usage="<text/voice>")
    async def create(self, ctx, choice: str):
        if await self.config.guild(ctx.guild).category_set() == True:

            admin_role = discord.utils.get(ctx.guild.roles, name="Administrator")
            head_admin_role = discord.utils.get(ctx.guild.roles, name="Head Admin")
            server_op_role = discord.utils.get(ctx.guild.roles, name="Server Operator")
            manager_role = discord.utils.get(ctx.guild.roles, name="Manager")

            if choice.lower() == "voice":
                channeltype = "voice"
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    ctx.author: discord.PermissionOverwrite(view_channel=True),
                    admin_role: discord.PermissionOverwrite(view_channel=True),
                    head_admin_role: discord.PermissionOverwrite(view_channel=True),
                    server_op_role: discord.PermissionOverwrite(view_channel=True),
                    manager_role: discord.PermissionOverwrite(view_channel=True)
                }
                ...
                if await self.config.member(ctx.author).has_voice_channel() == False:
                    await channel_creator(ctx, overwrites, channeltype)
                else:
                    await ctx.send(f"{ctx.author.mention} You already have a custom voice channel, are you sure you want to delete your existing one and create a new one? (yes/no)")
                    message = await self.bot.wait_for('message', check=authorcheck(ctx.author))
                    if message.content.lower() == "no":
                        pass
                    elif message.content.lower() == "yes":
                        ...
                        channel_to_delete = await channel_getter(ctx, channeltype)
                        if channel_to_delete != None:
                            async with self.config.guild(ctx.guild).custom_voice_channels() as custom_voice_channels:
                                if channel_to_delete.id in custom_voice_channels:
                                    custom_voice_channels.remove(channel_to_delete.id)
                                else:
                                    pass
                            await channel_to_delete.delete()
                        ...
                        
                        await channel_creator(ctx, overwrites, channeltype)
                        await ctx.send("Your custom voice channel has been created!")

            elif choice.lower() == "text":
                channeltype = "text"
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, attach_files=True, embed_links=True, use_external_emojis=True),
                    ctx.author: discord.PermissionOverwrite(read_messages=True, manage_messages=True, manage_permissions=True),
                    admin_role: discord.PermissionOverwrite(read_messages=True),
                    head_admin_role: discord.PermissionOverwrite(read_messages=True),
                    server_op_role: discord.PermissionOverwrite(read_messages=True),
                    manager_role: discord.PermissionOverwrite(read_messages=True)
                }
                ...
                if await self.config.member(ctx.author).has_text_channel() == False:
                    await channel_creator(ctx, overwrites, channeltype)
                else:
                    await ctx.send(f"{ctx.author.mention} You already have a custom text channel, are you sure you want to delete your existing one and create a new one? (yes/no)")
                    message = await self.bot.wait_for('message', check=authorcheck(ctx.author))
                    if message.content.lower() == "no":
                        pass
                    elif message.content.lower() == "yes":
                        ...
                        channel_to_delete = await channel_getter(ctx, channeltype)
                        if channel_to_delete != None:
                            async with self.config.guild(ctx.guild).custom_text_channels() as custom_text_channels:
                                if channel_to_delete.id in custom_text_channels:
                                    custom_text_channels.remove(
                                        channel_to_delete.id)
                                else:
                                    pass
                            await channel_to_delete.delete()
                        ...

                        await channel_creator(ctx, overwrites, channeltype)
                        await ctx.send("Your custom text channel has been created!")
        else:
            await ctx.send("Setup for this cog has not yet been complete. Ask the bot owner to complete the setup process.")
    ...
    @privatechannel.command(usage="<member> <text/voice>")
    async def add(self, ctx, member: discord.Member, choice: str):
        if choice.lower() == "voice":
            if await self.config.member(ctx.author).has_voice_channel() == True:
                ...
                channel = await channel_getter(ctx, channeltype=(choice.lower()))
                ...
                if channel != None:
                    await channel.set_permissions(member, view_channel=True)
                    try:
                        await ctx.send(f"Given **{member.name}** access to your custom voice channel")
                    except Exception:
                        pass
            else:
                await ctx.send("You have not created a custom voice channel yet.")
        elif choice.lower() == "text":
            if await self.config.member(ctx.author).has_text_channel() == True:
                ...
                channel = await channel_getter(ctx, channeltype=(choice.lower()))
                ...
                if channel != None:
                    await channel.set_permissions(member, read_messages=True, attach_files=True, embed_links=True, use_external_emojis=True)
                    try:
                        await ctx.send(f"Given **{member.name}** access to your custom text channel")
                    except Exception:
                        pass
            else:
                await ctx.send("You have not created a custom text channel yet.")
    ...
    @privatechannel.command(usage="<member> <text/voice>")
    async def remove(self, ctx, member: discord.Member, choice: str):
        if admin_check(member):
            if choice.lower() == "voice":
                if await self.config.member(ctx.author).has_voice_channel() == True:
                    ...
                    channel = await channel_getter(ctx, channeltype=(choice.lower()))
                    ...
                    if channel != None:
                        await channel.set_permissions(member, view_channel=False)
                        try:
                            await ctx.author.send(f"Stopped {member} from being able to access your custom voice channel")
                        except Exception:
                            pass
                else:
                    await ctx.send("You have not created a custom voice channel yet.")
            elif choice.lower() == "text":
                if await self.config.member(ctx.author).has_text_channel() == True:
                    ...
                    channel = await channel_getter(ctx, channeltype=(choice.lower()))
                    ...
                    if channel != None:
                        await channel.set_permissions(member, read_messages=False)
                        try:
                            await ctx.author.send(f"Stopped {member} from being able to access your custom text channel")
                        except Exception:
                            pass
                else:
                    await ctx.send("You have not created a custom text channel yet.")
        else:
            await ctx.send("You cannot target this member")
    ...
    @privatechannel.command(usage="<text/voice> [new_name]")
    async def rename(self, ctx, choice: str, *, name: str):
        if choice.lower() == "voice":
            try:
                if await self.config.member(ctx.author).has_voice_channel() == True:
                    ...
                    channel = await channel_getter(ctx, channeltype=(choice.lower()))
                    ...
                    if channel != None:
                        await channel.edit(name=name)
                        await ctx.send(f"Renamed your custom voice channel to **{name}**")
                else:
                    await ctx.send("You do not have a custom voice channel")
                    ...
            except Exception as e:
                print(e)
            finally:
                await ctx.send(f"Renamed your custom voice channel to **{name}**")
        elif choice.lower() == "text":
            try:
                if await self.config.member(ctx.author).has_text_channel() == True:
                    ...
                    channel = await channel_getter(ctx, channeltype=(choice.lower()))
                    ...
                    if channel != None:
                        await channel.edit(name=name)
                        await ctx.send(f"Renamed your custom text channel to **{name}**")
                else:
                    await ctx.send("You do not have a custom text channel")
                    ...
            except Exception as e:
                print(e)
    ...
    @privatechannel.command(usage="<text/voice>")
    async def delete(self, ctx, choice: str):
        if choice.lower() == "voice":
            if await self.config.member(ctx.author).has_voice_channel() == True:
                ...
                channel = await channel_getter(ctx, channeltype=(choice.lower()))
                ...
                if channel != None:
                    await channel.delete()

                async with self.config.guild(ctx.guild).custom_voice_channels() as custom_voice_channels:
                    if channel.id in custom_voice_channels:
                        custom_voice_channels.remove(channel.id)
                    else:
                        pass
                await self.config.member(ctx.author).has_voice_channel.set(False)
                await self.config.member(ctx.author).custom_voice_channel_id.set(0)
                await ctx.send("Deleted your custom voice channel")
            else:
                await ctx.send("You have not created a custom voice channel yet.")
        elif choice.lower() == "text":
            if await self.config.member(ctx.author).has_text_channel() == True:
                ...
                channel = await channel_getter(ctx, channeltype=(choice.lower()))
                ...
                if channel != None:
                    await channel.delete()

                async with self.config.guild(ctx.guild).custom_text_channels() as custom_text_channels:
                    if channel.id in custom_text_channels:
                        custom_text_channels.remove(channel.id)
                    else:
                        pass
                await self.config.member(ctx.author).has_text_channel.set(False)
                await self.config.member(ctx.author).custom_text_channel_id.set(0)
                await ctx.send("Deleted your custom text channel")
            else:
                await ctx.send("You have not created a custom voice channel yet.")
    ...
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after in before.guild.premium_subscribers and after not in after.guild.premium_subscribers:
            if await self.config.member(after).has_text_channel() == True:
                txt_id = await self.config.member(after).custom_text_channel_id()
                text_channel = discord.utils.get(after.guild.channels, id = txt_id)
                if text_channel != None:
                    await text_channel.delete()
            if await self.config.member(after).has_voice_channel() == True:
                voice_id = await self.config.member(after).custom_voice_channel_id()
                voice_channel = discord.utils.get(after.guild.channels, id=voice_id)
                if voice_channel != None:
                    await voice_channel.delete()
            if (await self.config.member(after).has_voice_channel() == True) or (await self.config.member(after).has_text_channel() == True):
                try:
                    await after.send("You are no longer boosting our guild, therefore your custom channel/s have been removed")
                except Exception:
                    pass
        else:
            pass
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if await self.config.member(member).has_voice_channel():
            channel_id = await self.config.member(member).custom_voice_channel_id()
            try:
                voice_channel = discord.utils.get(member.guild.voice_channels, id=channel_id)
                await voice_channel.delete()
                async with self.config.guild(member.guild).custom_voice_channels() as custom_voice:
                    if channel_id in custom_voice:
                        custom_voice.remove(channel_id)
            except:
                pass
        if await self.config.member(member).has_text_channel():
            channel_id = await self.config.member(member).custom_text_channel_id()
            try:
                text_channel= discord.utils.get(member.guild.text_channels, id=channel_id)
                await text_channel.delete()
                async with self.config.guild(member.guild).custom_text_channels() as custom_text:
                    if channel_id in custom_text:
                        custom_text.remove(channel_id)
            except:
                pass
