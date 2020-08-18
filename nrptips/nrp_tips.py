import asyncio, discord, datetime, time, string
from redbot.core import commands, checks, Config
from discord.ext import tasks
from discord.ext.commands import guild_only, has_any_role

def guild_check():
    async def checker(ctx):
        if ctx.message.guild.id == 699702073951912028:
            return True
    return commands.check(checker)

class NRPTips(commands.Cog):
    '''Looks for keywords/phrases within messages and responds based on pre-defined settings.'''

    __author__ = "Raff"
    __version__ = "2.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=55555552)
        default_guild = {
            "blacklisted_categories": [],
            "blacklisted_members": [],
            "logs_channel": None
        }
        self.config.register_guild(**default_guild)
        ...
        self.citizen_fx_ticket = "If you are receiving a message regarding Citizen FX Ticket, this will be due to FiveM's authentication servers being down.\n\nTo find out when it's back up, use https://lambda.fivem.net/ and the message contains \"CleanAndLegit\" then it is back up!"
        self.onesync_whitelist = "It seems like Patreon is having some issues connecting to our server. This could be due to some temporary downtime they may be having. This should resolve itself shortly and happens from time to time."
        ...
        self.due_to_respond = []
    ...
    # Setup & config commands
    ...
    @commands.command()
    @guild_check()
    @has_any_role("Owner", "Lead Admin")
    async def setnrplogchannel(self, ctx, channelid: int = None):
        if channelid != None:
            find_logs_channel = discord.utils.get(ctx.guild.text_channels, id=int(channelid))
            await self.config.guild(ctx.guild).logs_channel.set(find_logs_channel.id)
            await ctx.send(f"Set Tips-Cog logs channel as {find_logs_channel.mention}")
        else:
            await self.config.guild(ctx.guild).logs_channel.set(None)
            await ctx.send(f"Tips-Cog logs channel ID removed from config")
    @setnrplogchannel.error
    async def setnrplogchannel_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("That channel does not exist...")
    ...
    @commands.group(name="tnrpblacklist")
    @guild_check()
    @has_any_role("Owner", "Lead Admin")
    async def tips_blacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @tips_blacklist.command()
    async def category(self, ctx, category: int):
        category_object = discord.utils.get(ctx.guild.categories, id=category)
        async with self.config.guild(ctx.guild).blacklisted_categories() as categories:
            if category_object.id in categories:
                categories.remove(category_object.id)
                await ctx.send(f"`{category_object.name}` has been **removed** from the list of blacklisted categories.")
            else:
                categories.append(category_object.id)
                await ctx.send(f"`{category_object.name}` has been **added** to the list of blacklisted categories.")

    @tips_blacklist.command()
    async def member(self, ctx, member: discord.Member):
        async with self.config.guild(ctx.guild).blacklisted_members() as members:
            if member.id in members:
                members.remove(member.id)
                await ctx.send(f"{member.mention} has been **removed** from the list of blacklisted members.")
            else:
                members.append(member.id)
                await ctx.send(f"{member.mention} has been **added** to the list of blacklisted members.")
    ...
    ...
    @category.error
    async def tips_blacklist_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Category not found. Please enter a valid category ID.")
        else:
            pass

    @member.error
    async def tips_blacklist_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Member not found.")
        else:
            pass
    ...
    # Help & Question commands
    ...
    @commands.command()
    @guild_check()
    async def citizenfx(self, ctx):
        citizenfx = discord.Embed(title="No Citizen FX Ticket", description="{}".format(
            self.citizen_fx_ticket), color=0xff2f34)
        await ctx.send(embed=citizenfx)

    @commands.command()
    @guild_check()
    async def onesync(self, ctx):
        onesync = discord.Embed(title="OneSync is not whitelisted", description="{}".format(
            self.onesync_whitelist), color=0xff2f34)
        await ctx.send(embed=onesync)
    ...
    # Message reply
    ...
    @commands.Cog.listener()
    async def on_message(self, message):
        the_author = message.author
        if message.guild != None:
            if message.guild.id == 699702073951912028:
                async with self.config.guild(message.guild).blacklisted_categories() as categories:
                    async with self.config.guild(message.guild).blacklisted_members() as members:
                        if message.author.id not in members and message.channel.category.id not in categories and message.author.id not in self.due_to_respond:
                            message_words_original = message.content.split(" ")
                            message_words = []
                            for word in message_words_original:
                                message_words.append(word.lower())
                            ...
                            tick = discord.utils.get(message.guild.emojis, name = "tick")
                            cross = discord.utils.get(message.guild.emojis, name = "cross")
                            ...
                            continue_process = False
                            ...
                            tick_embed = discord.Embed(
                                title="Thank you for your feedback",
                                description="We're happy this helped fix your issue. If you have any more problems open a ticket using the <#269933786853015553> channel.",
                                timestamp=datetime.datetime.utcnow(),
                                colour=0x40eb34
                            )
                            cross_embed = discord.Embed(
                                title="Thank you for your feedback",
                                description="Sorry that this message did not help fix your issue or was not relevant to your message. If you think we could assist you further please open a ticket using the <#269933786853015553> channel.",
                                timestamp=datetime.datetime.utcnow(),
                                colour=0xff1f1f
                            )
                            timeout_embed = discord.Embed(
                                title="Run out of time to respond",
                                description="Although you did not give feedback in time, we hope this helped fix your issue. If not please open a ticket uting <#269933786853015553> so we can assist you further.",
                                timestamp=datetime.datetime.utcnow(),
                                colour=0x595959
                            )
                            ...
                            if ("citizen" in message_words) and ("fx" in message_words) and ("offline" in message_words):
                                support_embed = discord.Embed(
                                    title="No Citizen FX Ticket",
                                    description=f"{self.citizen_fx_ticket}\n\n**If this message was helpful, please react with a **{tick} **if not, react with a **{cross}**.**",
                                    timestamp=datetime.datetime.utcnow(),
                                    colour=0x37de07
                                )
                                continue_process = True
                                tip_given = "Citizen FX Ticket Tip"
                            elif ("onesync" in message_words) and ("whitelisted" in message_words) and ("onesync_plus" in message_words):
                                support_embed = discord.Embed(
                                    title="OneSync is not whitelisted",
                                    description=f"{self.onesync_whitelist}\n\n**If this message was helpful, please react with a **{tick} **if not, react with a **{cross}**.**",
                                    timestamp=datetime.datetime.utcnow(),
                                    colour=0x37de07
                                )
                                continue_process = True
                                tip_given = "OneSync Whitelist Tip"
                            ...
                            if continue_process:
                                self.due_to_respond.append(message.author.id)
                                sent_embed = await message.channel.send(content=message.author.mention, embed=support_embed)
                                await sent_embed.add_reaction(tick)
                                await sent_embed.add_reaction(cross)
                                ...
                                def check(reaction, user):
                                    return user == the_author and (reaction == tick or reaction == cross)
                                ...
                                try:
                                    reaction, user = await self.bot.wait_for('reaction_add', timeout=600, check=check)
                                except asyncio.TimeoutError:
                                    await sent_embed.edit(embed=timeout_embed)
                                    await sent_embed.clear_reactions()
                                    self.due_to_respond.remove(message.author.id)
                                else:
                                    logs_channel = discord.utils.get(message.guild.text_channels, id=await self.config.guild(message.guild).logs_channel())
                                    if reaction == tick and user == the_author:
                                        await reaction.message.edit(embed=tick_embed)
                                        await reaction.message.clear_reactions()

                                        helpful_embed = discord.Embed(
                                            description=f"[Go to message]({message.jump_url})",
                                            colour=0x40eb34,
                                            timestamp=datetime.datetime.utcnow()
                                        )
                                        helpful_embed.set_author(
                                            icon_url=message.author.avatar_url,
                                            name=f"{message.author.name} found this tip helpful"
                                        )
                                        helpful_embed.add_field(
                                            name="Tip Given",
                                            value=tip_given
                                        )
                                        self.due_to_respond.remove(message.author.id)
                                    elif reaction == cross and user == the_author:
                                        await reaction.message.edit(embed=cross_embed)
                                        await reaction.message.clear_reactions()

                                        helpful_embed = discord.Embed(
                                            description=f"[Go to message]({message.jump_url})",
                                            colour=0x40eb34,
                                            timestamp=datetime.datetime.utcnow()
                                        )
                                        helpful_embed.set_author(
                                            icon_url=message.author.avatar_url,
                                            name=f"{message.author.name} did not find this tip helpful"
                                        )
                                        helpful_embed.add_field(
                                            name="Tip Given",
                                            value=tip_given
                                        )
                                        self.due_to_respond.remove(message.author.id)
                                    try:
                                        await logs_channel.send(embed=helpful_embed)
                                    except:
                                        await message.channel.send(
                                            "Logs channel not found")
                                        pass
