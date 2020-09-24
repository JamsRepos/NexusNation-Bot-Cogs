import asyncio, discord, datetime, time, string
from redbot.core import commands, checks, Config
from discord.ext import tasks
from discord.ext.commands import guild_only, has_any_role

def guild_check():
    async def checker(ctx):
        if ctx.message.guild.id == 269912749327253504:
            return True
    return commands.check(checker)

class Tips(commands.Cog):
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
        self.no_map_msg = "If you are having trouble downloading maps from our servers or any other server for that matter, this is quite an easy fix. If you have ESEA, FACEIT, or CEVO client/AC open, exit these programs and ensure they are no longer running. Restart your game and try to rejoin."
        self.appeal_msg = "To appeal a punishment click [`here`](https://thenexusnation.com/appeal) and fill out all applicable boxes. Be sure to read the appeal rules before submitting."
        self.apply_msg = "To apply for staff click [`here`](https://thenexusnation.com/apply) and fill out all **all** boxes. Be sure to read the **application rules** before submitting."
        self.report_msg = "To report a player visit <#387538349663191041> and react to [this](https://discordapp.com/channels/269912749327253504/387538349663191041/645666639089500178) message. A ticket will then be opened where you can submit your player report"
        self.calladmin_msg = "If the player is still in the server please use `!calladmin` in game. If you are able to use something like shadowplay to gather evidence please do.\n If the member if no longer in the server please open a ticket in <#{}> and provide as much evidence as possible.".format(387538349663191041)
        self.differs_msg = "If you are kicked from the server with a message mentioning that your map differs from the servers do the following:\n1 - Navigate to your maps folder `SteamLibrary\\steamapps\\common\\Counter-Strike Global Offensive\\csgo\\maps`\n2 - Delete the map that differs from the servers\n3 - Try to reconnect to the server"
        self.vip_msg = "• Unique Rank in our Discord server\n• **Partial** Development Server Access\n• **2x** in game credits multiplier\n• **2** round arena challenge cooldown\n• **1x** vote extend per map\n• Ability to create a Custom VIP Tag\n• Combat Servers Ghost upon Death\n• Ability to talk in chat when dead on Jailbreak\n• VIP items on the Black Market & Federal Arsenal\n• Access to the VIP Area in the [In-Game Store](https://thenexusnation.com/store-guide)\n• Access to **!gloves**, **!mm**, **!pin** & **!level** commands\n• Access to **!tag**, **!squad** & **!gang** commands"
        self.vipplus_msg = "• Unique Rank in our Discord server\n• **Full** Development Server Access\n• **4x** in game credits multiplier\n• **0** round arena challenge cooldown\n• **3x** vote extend per map\n• Ability to create a Custom VIP Tag\n• Combat Servers Ghost upon Death\n• Ability to talk in chat when dead on Jailbreak\n• VIP items on the Black Market & Federal Arsenal\n• Access to the VIP Area in the [In-Game Store](https://thenexusnation.com/store-guide)\n• Access to **!gloves**, **!mm**, **!pin** & **!level** commands\n• Access to **!tag**, **!squad** & **!gang** commands\n• Ability to Set Text Colour\n• Force Next Map (!selectmap)\n• Double RTV/Map Votes\n• Access to **!votemute**, **!votegag** & **!votesilence** commands\n• Access to Fortnite & Twitch Emotes\n• Access to Any Weapon Skins"
        self.bug_msg = "To report a bug visit <#387538349663191041> and react to [this](https://discordapp.com/channels/269912749327253504/387538349663191041/645666644106149899) message. A ticket will then be opened where you can submit your bug report."
        self.leveltwo_msg = "You must be above level 2 (at least level 3) on CS:GO in order to play on our servers.\nIf you are not yet level 2 and wish to play on our servers, you should play some deathmatch/casual games to level up!\n\nBy purchasing [VIP](https://thenexusnation.com/store) you are able to bypass this check and will be able to join our servers no matter your level."
        self.suggest_msg = "To make a suggestion, visit the <#269933786853015553> channel and type `!suggest` followed by your suggestion"
        ...
        self.due_to_respond = []
    ...
    # Setup & config commands
    ...
    @commands.command()
    @guild_check()
    @has_any_role("Owner","Server Operator","Manager","Head Admin","Administrator")
    async def setlogchannel(self, ctx, channelid: int = None):
        if channelid != None:
            find_logs_channel = discord.utils.get(ctx.guild.text_channels, id=int(channelid))
            await self.config.guild(ctx.guild).logs_channel.set(find_logs_channel.id)
            await ctx.send(f"Set Tips-Cog logs channel as {find_logs_channel.mention}")
        else:
            await self.config.guild(ctx.guild).logs_channel.set(None)
            await ctx.send(f"Tips-Cog logs channel ID removed from config")
    @setlogchannel.error
    async def setlogchannel_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("That channel does not exist...")
    ...
    @commands.group(name="tblacklist")
    @guild_check()
    @has_any_role("Owner", "Server Operator", "Manager", "Head Admin", "Administrator")
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
    async def missing(self, ctx):
        nomapembed = discord.Embed(title="Map Download Issues", description="{}".format(
            self.no_map_msg), color=0xff2f34)
        await ctx.send(embed=nomapembed)

    @commands.command()
    @guild_check()
    async def appeal(self, ctx):
        nomapembed = discord.Embed(title="How to appeal a punishment", description="{}".format(
            self.appeal_msg), color=0xff2f34)
        await ctx.send(embed=nomapembed)

    @commands.command()
    @guild_check()
    async def apply(self, ctx):
        nomapembed = discord.Embed(title="How to apply for staff", description="{}".format(
            self.apply_msg), color=0xff2f34)
        await ctx.send(embed=nomapembed)

    @commands.command()
    @guild_check()
    async def report(self, ctx):
        nomapembed = discord.Embed(title="How to report a player", description="{}".format(
            self.report_msg), color=0xff2f34)
        await ctx.send(embed=nomapembed)

    @commands.command()
    @guild_check()
    async def calladmin(self, ctx):
        nomapembed = discord.Embed(title="How to use calladmin", description="{}".format(
            self.calladmin_msg), color=0xff2f34)
        await ctx.send(embed=nomapembed)

    @commands.command()
    @guild_check()
    async def differs(self, ctx):
        nomapembed = discord.Embed(title="Map Differs Issue", description="{}".format(
            self.differs_msg), color=0xff2f34)
        await ctx.send(embed=nomapembed)

    @commands.command()
    @guild_check()
    async def bugreport(self, ctx):
        nomapembed = discord.Embed(title="How to report a bug", description="{}".format(
            self.bug_msg), color=0xff2f34)
        await ctx.send(embed=nomapembed)
    ...
    @commands.command()
    @guild_check()
    @commands.cooldown(1, 180, commands.BucketType.guild)
    async def vip(self, ctx):
        vip_embed = discord.Embed(color=0xff2f34,timestamp=datetime.datetime.utcnow())
        vip_embed.set_author(name="VIP/VIP+ Information", url="https://nexushub.io/", icon_url="https://thenexusnation.com/img/logo.png")
        vip_embed.add_field(name="Information", value="Purchase VIP or VIP+ by visiting the NexusNation [store](https://nexushub.io/).", inline=False)
        vip_embed.add_field(name="VIP Features", value="{}".format(self.vip_msg), inline=True)
        vip_embed.add_field(name="VIP +Features", value="{}".format(self.vipplus_msg), inline=True)
        await ctx.message.delete()
        await ctx.send(embed=vip_embed)
    ...
    # Message reply
    ...
    @commands.Cog.listener()
    async def on_message(self, message):
        the_author = message.author
        if message.guild != None:
            if message.guild.id == 687040596149272595:
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
                            if ("map" in message_words) and ("missing" in message_words):
                                support_embed = discord.Embed(
                                    title="Missing Map",
                                    description=f"{self.no_map_msg}\n\n**If this message was helpful, please react with a **{tick} **if not, react with a **{cross}**.**",
                                    timestamp=datetime.datetime.utcnow(),
                                    colour=0x03e8fc
                                )
                                continue_process = True
                                tip_given = "Missing map tip"
                            elif ("how" in message_words) and (("can" in message_words) or ("do" in message_words)) \
                                    and (("appeal" in message_words) or ("unban" in message_words) or ("unmute" in message_words) or ("ungag" in message_words) \
                                        or ("un-ban" in message_words) or ("un-mute" in message_words) or ("un-gag" in message_words)) \
                                            or ("un" in message_words and ("ban" in message_words or "gag" in message_words or "mute" in message_words) and ("!suggest" != message_words[0])):
                                support_embed = discord.Embed(
                                    title="Appealing a punishment",
                                    description=f"{self.appeal_msg}\n\n**If this message was helpful, please react with a **{tick} **if not, react with a **{cross}**.**",
                                    timestamp=datetime.datetime.utcnow(),
                                    colour=0x03e8fc
                                )
                                continue_process = True
                                tip_given = "Appealing a punishment tip"
                            elif ("map" in message_words) and (("differs" in message_words) or ("differ" in message_words) and ("!suggest" != message_words[0])):
                                support_embed = discord.Embed(
                                    title="Map Differs",
                                    description=f"{self.differs_msg}\n\n**If this message was helpful, please react with a **{tick} **if not, react with a **{cross}**.**",
                                    timestamp=datetime.datetime.utcnow(),
                                    colour=0x03e8fc
                                )
                                continue_process = True
                                tip_given = "Map differs tip"
                            elif ("how" in message_words) and (("can" in message_words) or ("do" in message_words)) \
                                    and ("i" in message_words) and ("suggest" in message_words) \
                                        and ("!suggest" != message_words[0]):
                                support_embed = discord.Embed(
                                    title="Submitting a suggestion",
                                    description=f"{self.suggest_msg}\n\n**If this message was helpful, please react with a **{tick} **if not, react with a **{cross}**.**",
                                    timestamp=datetime.datetime.utcnow(),
                                    colour=0x03e8fc
                                )
                                continue_process = True
                                tip_given = "How to suggest tip"
                            elif ("there" in message_words) and ("is" in message_words) and (("hacker" in message_words) or ("spam" in message_words) or ("spammer" in message_words)):
                                support_embed = discord.Embed(
                                    title="Using !calladmin",
                                    description=f"{self.calladmin_msg}\n\n**If this message was helpful, please react with a **{tick} **if not, react with a **{cross}**.**",
                                    timestamp=datetime.datetime.utcnow(),
                                    colour=0x03e8fc
                                )
                                continue_process = True
                                tip_given = "How to calladmin tip"
                            elif ("how" in message_words) and (("can" in message_words) or ("do" in message_words)) \
                                    and ("i" in message_words) and ("report" in message_words) and ("!suggest" != message_words[0]):
                                support_embed = discord.Embed(
                                    title="Submitting a report",
                                    timestamp=datetime.datetime.utcnow(),
                                    colour=0x03e8fc
                                )
                                support_embed.add_field(
                                    name="Reporting a player",
                                    value=self.report_msg,
                                    inline=False
                                )
                                support_embed.add_field(
                                    name="Reporting a bug",
                                    value=f"{self.bug_msg}\n\n**If this message was helpful, please react with a **{tick} **if not, react with a **{cross}**.**",
                                    inline=False
                                )
                                continue_process = True
                                tip_given = "How to report tip"
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
