import aiohttp, json, asyncio, discord, datetime, time, string, json
from redbot.core import commands, checks, Config
from discord.ext import tasks

def is_staff_member():
    async def checker(ctx):
        async with ctx.cog.config.moderator_level() as md:
            for x in ctx.author.roles:
                if x.id in md:
                    return True
                elif len(md) < 1:
                    return True
    return commands.check(checker)

def is_admin_plus():
    async def checker(ctx):
        async with ctx.cog.config.admin_level() as adm:
            for x in ctx.author.roles:
                if x.id in adm:
                    return True
                elif len(adm) < 1:
                    return True
    return commands.check(checker)


def guild_check():
    async def checker(ctx):
        if ctx.message.guild.id == 269912749327253504:
            return True
    return commands.check(checker)


class Tips(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.now = datetime.datetime.now()
        self.config = Config.get_conf(self, identifier=1334567890)
        default_global = {
            "bads": [],
            "whitelist": [],
            "logs_channel": 0,
            "disallowed_categories": [],
            "disallowed_member_ids": [],
            "moderator_level": [],
            "admin_level": []
        }

        self.config.register_global(**default_global)
        self.no_map_msg = "If you are having trouble downloading maps from our servers or any other server for that matter, this is quite an easy fix. If you have ESEA, FACEIT, or CEVO client/AC open, exit these programs and ensure they are no longer running. Restart your game and try to rejoin."
        self.appeal_msg = "To appeal a punishment click [`here`](https://thenexusnation.com/appeal) and fill out all applicable boxes. Be sure to read the appeal rules before submitting."    
        self.apply_msg = "To apply for staff click [`here`](https://thenexusnation.com/apply) and fill out all **all** boxes. Be sure to read the **application rules** before submitting." 
        self.report_msg = "To report a player go to <#387538349663191041> and open a ticket relating to your issue."
        self.calladmin_msg = "If the player is still in the server please use `!calladmin` in game. If you are able to use something like shadowplay to gather evidence please do.\n If the member if no longer in the server please open a ticket in <#{}> and provide as much evidence as possible.".format(387538349663191041)
        self.differs_msg = "If you are kicked from the server with a message mentioning that your map differs from the servers do the following:\n1 - Navigate to your maps folder `SteamLibrary\\steamapps\\common\\Counter-Strike Global Offensive\\csgo\\maps`\n2 - Delete the map that differs from the servers\n3 - Try to reconnect to the server"
        self.vip_msg = "• Unique Rank in our Discord server\n• **Partial** Development Server Access\n• **2x** in game credits multiplier\n• **2** round arena challenge cooldown\n• **1x** vote extend per map\n• Ability to create a Custom VIP Tag\n• Combat Servers Ghost upon Death\n• Ability to talk in chat when dead on Jailbreak\n• VIP items on the Black Market & Federal Arsenal\n• Access to the VIP Area in the [In-Game Store](https://thenexusnation.com/store-guide)\n• Access to **!gloves**, **!mm**, **!pin** & **!level** commands\n• Access to **!tag**, **!squad** & **!gang** commands"
        self.vipplus_msg = "• Unique Rank in our Discord server\n• **Full** Development Server Access\n• **4x** in game credits multiplier\n• **0** round arena challenge cooldown\n• **3x** vote extend per map\n• Ability to create a Custom VIP Tag\n• Combat Servers Ghost upon Death\n• Ability to talk in chat when dead on Jailbreak\n• VIP items on the Black Market & Federal Arsenal\n• Access to the VIP Area in the [In-Game Store](https://thenexusnation.com/store-guide)\n• Access to **!gloves**, **!mm**, **!pin** & **!level** commands\n• Access to **!tag**, **!squad** & **!gang** commands\n• Ability to Set Text Colour\n• Force Next Map (!selectmap)\n• Double RTV/Map Votes\n• Access to **!votemute**, **!votegag** & **!votesilence** commands\n• Access to Fortnite & Twitch Emotes\n• Access to Any Weapon Skins"
        self.bug_msg = "To report a bug use the command `!bug` followed by one of our server names and your bug report.\nThe finished command should look something like this `!bug jailbreak reason`"
        self.leveltwo_msg = "You must be above level 2 (at least level 3) on CS:GO in order to play on our servers.\nIf you are not yet level 2 and wish to play on our servers, you should play some deathmatch/casual games to level up!\n\nBy purchasing [VIP](https://thenexusnation.com/store) you are able to bypass this check and will be able to join our servers no matter your level."
        self.suggest_msg = "To make a suggestion, visit the <#269933786853015553> channel and type `!suggest` followed by your suggestion"
        self.command_maker = []
        self.addreaction = False
        self.continue_instance = False

    @commands.command()
    @is_admin_plus()
    @guild_check()
    async def addstaffrole(self, ctx, staffrole: int):
        async with self.config.moderator_level() as moderator_and_above:
            if staffrole not in moderator_and_above:
                moderator_and_above.append(staffrole)
                await ctx.send(f"Added <@&{staffrole}> to the staff roles list.")
            elif staffrole in moderator_and_above:
                await ctx.send(f"<@&{staffrole}> already in staff roles list.")

    @commands.command()
    @is_admin_plus()
    @guild_check()
    async def removestaffrole(self, ctx, staffrole: int):
        async with self.config.moderator_level() as moderator_and_above:
            if staffrole in moderator_and_above:
                moderator_and_above.remove(staffrole)
                await ctx.send(f"Removed <@&{staffrole}> from the staff roles list.")
            elif staffrole not in moderator_and_above:
                await ctx.send(f"<@&{staffrole}> not in the staff roles list.")


    @commands.command()
    @is_admin_plus()
    @guild_check()
    async def addadminrole(self, ctx, staffrole: int):
        async with self.config.admin_level() as admin_and_above:
            if staffrole not in admin_and_above:
                admin_and_above.append(staffrole)
                await ctx.send(f"Added <@&{staffrole}> to the admin+ roles list.")
            elif staffrole in admin_and_above:
                await ctx.send(f"<@&{staffrole}> already in admin+ roles list.")

    @commands.command()
    @is_admin_plus()
    @guild_check()
    async def removeadminrole(self, ctx, staffrole: int):
        async with self.config.admin_level() as admin_and_above:
            if staffrole in admin_and_above:
                admin_and_above.remove(staffrole)
                await ctx.send(f"Removed <@&{staffrole}> from the admin+ roles list.")
            elif staffrole not in admin_and_above:
                await ctx.send(f"<@&{staffrole}> not in the admin+ roles list.")


    @commands.command()
    @is_admin_plus()
    @guild_check()
    async def addword(self, ctx, new_word: str):
        async with self.config.bads() as bads:
            if (new_word).lower() not in bads:
                bads.append(str((new_word).lower()))
                await ctx.send(f"You have added '{new_word}' to the forbidden words list.")
            elif (new_word).lower() in bads:
                await ctx.send(f"'{new_word}' already recognised as a forbidden word.")
        
    @commands.command()
    @is_admin_plus()
    @guild_check()
    async def addwords(self, ctx, *, words: str):
        wordz = words.split()
        wordz = list(dict.fromkeys(wordz))
        wordz.sort()
        async with self.config.bads() as bads:
            for word in wordz:
                if word in bads:
                    wordz.remove(word)
                elif word not in bads:
                    bads.append(word)
            bads.sort()
            await ctx.send(f"Added the following words to the forbidden words list: {', '.join(wordz)}")


    @commands.command()
    @is_admin_plus()
    @guild_check()
    async def removeword(self, ctx, old_word: str):
        async with self.config.bads() as bads:
            if (old_word).lower() in bads:
                bads.remove(str(old_word))
                await ctx.send(f"'{old_word}' has been removed from the forbidden words list.")
            elif (old_word).lower() not in bads:
                await ctx.send(f"'{old_word}' is not in the forbidden words list.")

    @commands.command()
    @is_admin_plus()
    @guild_check()
    async def whitelistadd(self, ctx, channelid: int):
        async with self.config.whitelist() as whitelist:
            if channelid not in whitelist:
                whitelist.append(channelid)
                await ctx.send(f"{channelid} added to the whitelist.")
            elif channelid in whitelist:
                await ctx.send(f"{channelid} already in whitelist.")


    @commands.command()
    @is_admin_plus()
    @guild_check()
    async def whitelistremove(self, ctx, channelid: int):
        async with self.config.whitelist() as whitelist:
            if channelid in whitelist:
                whitelist.remove(channelid)
                await ctx.send(f"{channelid} has been removed from the forbidden words list.")
            elif channelid not in whitelist:
                await ctx.send(f"{channelid} is not in the forbidden words list.")

    @commands.command()
    @is_admin_plus()
    @guild_check()
    async def setlogschannel(self, ctx, channelid: int):
        await self.config.logs_channel.set(channelid)
        await ctx.send(f"Logs channel set as <#{channelid}>")

    @commands.command()
    @is_admin_plus()
    @guild_check()
    async def disallowmember(self, ctx, memberid: int):
        async with self.config.disallowed_member_ids() as disallowed:
            if memberid not in disallowed:
                disallowed.append(memberid)
                await ctx.send(f"<@!{memberid}> added to the disallow list.")
            elif memberid in disallowed:
                await ctx.send(f"<@!{memberid}> already in the disallow list.")

    @commands.command()
    @is_admin_plus()
    @guild_check()
    async def allowmember(self, ctx, memberid: int):
        async with self.config.disallowed_member_ids() as disallowed:
            if memberid in disallowed:
                disallowed.remove(memberid)
                await ctx.send(f"<@!{memberid}> removed from the disallow list.")
            elif memberid not in disallowed:
                await ctx.send(f"<@!{memberid}> not in the disallow list.")


    @commands.command()
    @is_admin_plus()
    @guild_check()
    async def disallowcategory(self, ctx, categoryid: int):
        async with self.config.disallowed_categories() as disallowed:
            if categoryid not in disallowed:
                disallowed.append(categoryid)
                await ctx.send(f"{categoryid} added to the category disallow list.")
            elif categoryid in disallowed:
                await ctx.send(f"{categoryid} already in the category disallow list.")

    @commands.command()
    @is_admin_plus()
    @guild_check()
    async def allowcategory(self, ctx, categoryid: int):
        async with self.config.disallowed_categories() as disallowed:
            if categoryid in disallowed:
                disallowed.remove(categoryid)
                await ctx.send(f"{categoryid} removed from the category disallow list.")
            elif categoryid not in disallowed:
                await ctx.send(f"{categoryid} not in the category disallow list.")
            


    @commands.command()
    @is_staff_member()
    @guild_check()
    async def returndata(self, ctx):
        
        data = discord.Embed(
            title="Tips Cog Config Data",
             color=0xFF06FF
             )
        async with self.config.bads() as bads:
            if len(bads)>=1:
                data.add_field(
                    name="Forbidden words",
                    value=(', '.join(bads)),
                    inline=False
                    )
        async with self.config.whitelist() as whitelist:
            if len(whitelist)>=1:
                string = ""
                for i in range(len(whitelist)):
                    string += f" <#{whitelist[i]}>"
                data.add_field(
                    name="Whitelisted channels",
                    value=(string),
                    inline=False
                    )
        data.add_field(
            name="Tips Cog Logs Channel",
            value=(f"<#{await self.config.logs_channel()}>"),
                    inline=False
            )       
        async with self.config.disallowed_member_ids() as dmis:
            if len(dmis)>=1:
                string_members = ""
                for i in range(len(dmis)):
                    string_members += f" <@!{dmis[i]}>"
                data.add_field(
                    name="Disallowed Members",
                    value=(string_members),
                    inline=False
                    )    
        async with self.config.disallowed_categories() as dc:
            if len(dc)>=1:
                data.add_field(
                    name="Disallowed Categories",
                    value=((str(dc).replace("[","")).replace("]","")),
                    inline=False
                    )    
        async with self.config.moderator_level() as md:
            if len(md) >=1:
                string_staff = ""
                for i in range(len(md)):
                    string_staff +=f" <@&{md[i]}>"
                data.add_field(
                    name="Staff Roles",
                    value=(string_staff),
                    inline=False
                )
        async with self.config.admin_level() as adm:
            if len(md) >=1:
                string_admin = ""
                for i in range(len(adm)):
                    string_admin +=f" <@&{adm[i]}>"
                data.add_field(
                    name="Admin+ Roles",
                    value=(string_admin),
                    inline=False
                )
        await ctx.send(
            content="Current Tips Config",
            embed=data
            )
            
    @commands.command()
    @is_staff_member()
    @guild_check()
    async def missing(self, ctx):
        nomapembed=discord.Embed(title="Map Download Issues", description="{}".format(self.no_map_msg), color=0xff2f34)
        await ctx.send(embed=nomapembed)
        
    @commands.command()
    @is_staff_member()
    @guild_check()
    async def appeal(self, ctx):
        nomapembed=discord.Embed(title="How to appeal a punishment", description="{}".format(self.appeal_msg), color=0xff2f34)
        await ctx.send(embed=nomapembed)

    @commands.command()
    @is_staff_member()
    @guild_check()
    async def apply(self, ctx):
        nomapembed=discord.Embed(title="How to apply for staff", description="{}".format(self.apply_msg), color=0xff2f34)
        await ctx.send(embed=nomapembed)

    @commands.command()
    @is_staff_member()
    @guild_check()
    async def report(self, ctx):
        nomapembed=discord.Embed(title="How to report a player", description="{}".format(self.report_msg), color=0xff2f34)
        await ctx.send(embed=nomapembed)

    @commands.command()
    @is_staff_member()
    @guild_check()
    async def calladmin(self, ctx):
        nomapembed=discord.Embed(title="How to use calladmin", description="{}".format(self.calladmin_msg), color=0xff2f34)
        await ctx.send(embed=nomapembed)

    @commands.command()
    @is_staff_member()
    @guild_check()
    async def differs(self, ctx):
        nomapembed=discord.Embed(title="Map Differs Issue", description="{}".format(self.differs_msg), color=0xff2f34)
        await ctx.send(embed=nomapembed)

    @commands.command()
    @is_staff_member()
    @guild_check()
    async def bugreport(self, ctx):
        nomapembed=discord.Embed(title="How to report a bug", description="{}".format(self.bug_msg), color=0xff2f34)
        await ctx.send(embed=nomapembed)

    @commands.command()
    @is_staff_member()
    @guild_check()
    async def clr_list(self, ctx):
        self.command_maker.clear()
        await ctx.send("List cleared")

    @commands.command()
    @guild_check()
    @commands.cooldown(1, 180, commands.BucketType.guild)
    async def vip(self, ctx):
        vip_embed = discord.Embed(color=0xff2f34)
        vip_embed.set_author(name="VIP/VIP+ Information", url="https://nexushub.io/", icon_url="https://thenexusnation.com/img/logo.png")
        vip_embed.add_field(name="Information", value="Purchase VIP or VIP+ by visiting the NexusNation [store](https://nexushub.io/).", inline=False)
        vip_embed.add_field(name="VIP Features", value="{}".format(self.vip_msg), inline=True)
        vip_embed.add_field(name="VIP +Features", value="{}".format(self.vipplus_msg), inline=True)
        vip_embed.set_footer(text="TheNexusNation.com • {} {}".format(self.now.strftime("%d/%m/%Y"), self.now.strftime("%H:%M")))
        await ctx.message.delete()
        await ctx.send(embed=vip_embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        self.continue_instance = False
        bad_reaction_one = discord.Embed(title="Thanks for your feedback", description="Sorry to hear that your problem has not been fixed <@!{}>. Please open a ticket in <#689913408979468293> for further assistance".format(message.author.id), color=0x000000)
        bad_reaction_two = discord.Embed(title="Thanks for your feedback",description="This will help us improve the bot.", color=0x000000)
        bad_reaction_two.set_thumbnail(url="https://media1.tenor.com/images/8b5f9ae2d38e55483bf4cb1d01c281e6/tenor.gif")
        bad_reaction_two.set_footer(text="TheNexusNation.com • {} {}".format(self.now.strftime("%d/%m/%Y"), self.now.strftime("%H:%M")))
        timed_out = discord.Embed(title="We hope this helped fix your problem", description="Although you did not give feedback in time, we hope this message helped fix your problem.\n\nIf you have any other questions or need any more help please open a ticket in <#387538349663191041>",color=0x06ff00)

####################################################################################-RESPONSES-######################################################################################################
        if message.guild.id == 269912749327253504:
            if ('map' in (str(message.content).lower()) and 'missing' in (str(message.content).lower())) and (message.channel.category.id not in await self.config.disallowed_categories()) and (message.author.id not in await self.config.disallowed_member_ids()):
                if message.author.id not in self.command_maker:

                    self.embed=discord.Embed(title="Map Download Issues", description="{}\n\n**If this message was helpful, please react with a **<:tick:445640284202729472> **if not, react with a **<:cross:445640325780865035>**.**".format(self.no_map_msg), color=0x626262)
                    embed_green=discord.Embed(title="Map Download Issues", description="{}\n\n**Thank you for your feedback • TheNexusNation.com**".format(self.no_map_msg), color=0x06ff00)
                    self.embed = await message.channel.send(
                        content=message.author.mention,
                        embed=self.embed
                        )
                    self.addreaction = True
                    self.command_maker.append(message.author.id)
                    self.continue_instance = True
                else:
                    await message.channel.send("<@!{}> please react to the bots last response.".format(message.author.id))

            elif (('can' in (str(message.content).lower()) or 'do' in (str(message.content).lower())) and 'i' in (str(message.content).lower()) and ((('get' in (str(message.content).lower()) or 'be' in (str(message.content).lower())) and ('un' in (str(message.content).lower()) and ('ban' in (str(message.content).lower())) or 'mute' in (str(message.content).lower()) or'gag' in (str(message.content).lower())) or 'appeal' in (str(message.content).lower()))) and (message.channel.category.id not in await self.config.disallowed_categories()) and (message.author.id not in await self.config.disallowed_member_ids())):
                if message.author.id not in self.command_maker:
                    
                    self.embed=discord.Embed(title="Appealing a punishment", description="{}\n\n**If this message was helpful, please react with a **<:tick:445640284202729472> **if not, react with a **<:cross:445640325780865035>**.**".format(self.appeal_msg), color=0x626262)
                    embed_green=discord.Embed(title="Appealing a punishment", description="{}\n\n**Thank you for your feedback • TheNexusNation.com**".format(self.appeal_msg), color=0x06ff00)
                    self.embed = await message.channel.send(
                        content=message.author.mention,
                        embed=self.embed
                        )
                    self.addreaction = True
                    self.command_maker.append(message.author.id)    
                    self.continue_instance = True           
                else:
                    await message.channel.send("<@!{}> please react to the bots last response.".format(message.author.id))

            elif 'how'in (str(message.content).lower()) and ('can' in (str(message.content).lower()) or 'do' in (str(message.content).lower())) and 'i' in (str(message.content).lower()) and'apply' in (str(message.content).lower()) and (message.channel.category.id not in await self.config.disallowed_categories()) and (message.author.id not in await self.config.disallowed_member_ids()):
                if message.author.id not in self.command_maker:

                    self.embed=discord.Embed(title="Applying for staff", description="{}\n\n**If this message was helpful, please react with a **<:tick:445640284202729472> **if not, react with a **<:cross:445640325780865035>**.**".format(self.apply_msg), color=0x626262)
                    embed_green=discord.Embed(title="Applying for staff", description="{}\n\n**Thank you for your feedback • TheNexusNation.com**".format(self.apply_msg), color=0x06ff00)
                    self.embed = await message.channel.send(
                        content=message.author.mention,
                        embed=self.embed
                        )
                    self.addreaction = True
                    self.command_maker.append(message.author.id) 
                    self.continue_instance = True               
                else:
                    await message.channel.send("<@!{}> please react to the bots last response.".format(message.author.id))

            elif ('want' in (str(message.content).lower()) or 'can' in (str(message.content).lower()) or 'do' in (str(message.content).lower())) and 'i' in (str(message.content).lower()) and ('report' in (str(message.content).lower()) and (message.channel.category.id not in await self.config.disallowed_categories()) and (message.author.id not in await self.config.disallowed_member_ids())):
                if message.author.id not in self.command_maker:

                    self.embed=discord.Embed(title="Reporting a player/bug", description="{}\n\n**If this message was helpful, please react with a **<:tick:445640284202729472> **if not, react with a **<:cross:445640325780865035>**.**".format(self.report_msg), color=0x626262)
                    embed_green=discord.Embed(title="Reporting a player/bug", description="{}\n\n**Thank you for your feedback • TheNexusNation.com**".format(self.report_msg), color=0x06ff00)
                    self.embed = await message.channel.send(
                        content=message.author.mention,
                        embed=self.embed
                        )
                    self.addreaction = True
                    self.command_maker.append(message.author.id)
                    self.continue_instance = True
                else:
                    await message.channel.send("<@!{}> please react to the bots last response.".format(message.author.id))

            elif (('there' in str(message.content).lower() and 'is' in str(message.content).lower() and ('hacker' in str(message.content).lower() or 'spam' in str(message.content).lower() or 'cheater' in str(message.content).lower() or 'freekill' in str(message.content).lower()) and (message.channel.category.id not in await self.config.disallowed_categories()) and (message.author.id not in await self.config.disallowed_member_ids()))):
                if message.author.id not in self.command_maker:

                    self.embed=discord.Embed(title="Using !calladmin", description="{}\n\n**If this message was helpful, please react with a **<:tick:445640284202729472> **if not, react with a **<:cross:445640325780865035>**.**".format(self.calladmin_msg), color=0x626262)
                    embed_green=discord.Embed(title="Using !calladmin", description="{}\n\n**Thank you for your feedback • TheNexusNation.com**".format(self.calladmin_msg), color=0x06ff00)
                    self.embed = await message.channel.send(
                        content=message.author.mention,
                        embed=self.embed
                        )
                    self.addreaction = True
                    self.command_maker.append(message.author.id)
                    self.continue_instance = True
                else:
                    await message.channel.send("<@!{}> please react to the bots last response.".format(message.author.id))

            elif ('map' in (str(message.content).lower()) and 'differs' in (str(message.content).lower())) and (message.channel.category.id not in self.config.disallowed_categories()) and (message.author.id not in self.config.disallowed_member_ids()):
                if message.author.id not in self.command_maker:

                    self.embed=discord.Embed(title="Map Differs Issue", description="{}\n\n**If this message was helpful, please react with a **<:tick:445640284202729472> **if not, react with a **<:cross:445640325780865035>**.**".format(self.differs_msg), color=0x626262)
                    embed_green=discord.Embed(title="Map Differs Issue", description="{}\n\n**Thank you for your feedback • TheNexusNation.com**".format(self.differs_msg), color=0x06ff00)
                    self.embed = await message.channel.send(
                        content=message.author.mention,
                        embed=self.embed
                        )
                    self.addreaction = True
                    self.command_maker.append(message.author.id)
                    self.continue_instance = True
                else:
                    await message.channel.send("<@!{}> please react to the bots last response.".format(message.author.id))

            elif ('says' in (str(message.content).lower()) or 'asks' in (str(message.content).lower())) and ('level' in (str(message.content).lower()) or 'lvl' in (str(message.content).lower())) and ('2' in (str(message.content).lower()) or 'two' in (str(message.content).lower())) and (message.channel.category.id not in await self.config.disallowed_categories()) and (message.author.id not in await self.config.disallowed_member_ids()):
                if message.author.id not in self.command_maker:

                    self.embed=discord.Embed(title="Must Be Level Above Level 2", description="{}\n\n**If this message was helpful, please react with a **<:tick:445640284202729472> **if not, react with a **<:cross:445640325780865035>**.**".format(self.leveltwo_msg), color=0x626262)
                    embed_green=discord.Embed(title="Must Be Level Above Level 2", description="{}\n\n**Thank you for your feedback • TheNexusNation.com**".format(self.leveltwo_msg), color=0x06ff00)
                    self.embed = await message.channel.send(
                        content=message.author.mention,
                        embed=self.embed
                        )
                    self.addreaction = True
                    self.command_maker.append(message.author.id)
                    self.continue_instance = True
                else:
                    await message.channel.send("<@!{}> please react to the bots last response.".format(message.author.id))
                    
            elif (('can' in (str(message.content).lower()) or 'do' in (str(message.content).lower())) and 'i' in (str(message.content).lower()) and ('suggest' in (str(message.content).lower()) and (message.channel.category.id not in await self.config.disallowed_categories()) and (message.author.id not in await self.config.disallowed_member_ids()))):
                if message.author.id not in self.command_maker:

                    self.embed = discord.Embed(title="How to make a suggestion",
                                            description="{}\n\n**If this message was helpful, please react with a **<:tick:445640284202729472> **if not, react with a **<:cross:445640325780865035>**.**".format(self.suggest_msg), color=0x626262)
                    embed_green = discord.Embed(title="How to make a suggestion",
                                                description="{}\n\n**Thank you for your feedback • TheNexusNation.com**".format(self.suggest_msg), color=0x06ff00)
                    self.embed = await message.channel.send(
                        content=message.author.mention,
                        embed=self.embed
                    )
                    self.addreaction = True
                    self.command_maker.append(message.author.id)
                    self.continue_instance = True
                else:
                    await message.channel.send("<@!{}> please react to the bots last response.".format(message.author.id))
            else:
                sent_message = str(message.content).split()
                bad_words = await self.config.bads()
                whitelisted_channels = await self.config.whitelist()
                if int(message.channel.id) not in whitelisted_channels:
                    for word in bad_words:
                        if (word in (sent_message)) or (word+"s" in (sent_message)):
                            embedBadWord=discord.Embed(description="This message was flagged for a forbidden phrase.", color=0xff00d0)
                            embedBadWord.set_author(name="{} has said a forbidden phrase.".format(message.author),icon_url=message.author.avatar_url)
                            embedBadWord.add_field(name="Original Message", value=str(message.content), inline=False)
                            embedBadWord.set_footer(text="TheNexusNation.com • {} {}".format(self.now.strftime("%d/%m/%Y"), self.now.strftime("%H:%M")))
                            await self.bot.get_channel(await self.config.logs_channel()).send(embed=embedBadWord)
                            await message.channel.send("<@!{}> please refrain from saying that.".format(message.author.id))
                            await message.delete()
                            break





    ######################################################################################################################################################################################################

            if self.continue_instance == True:
                if self.addreaction == True:
                    await self.embed.add_reaction(emoji = "<:tick:445640284202729472>")
                    await self.embed.add_reaction(emoji = "<:cross:445640325780865035>")
                    self.addreaction = False

                def check(reaction, user):
                    return user == message.author and (str(reaction) == '<:tick:445640284202729472>' or str(reaction) == '<:cross:445640325780865035>')
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=900, check=check)
                    if str(reaction) == '<:tick:445640284202729472>' and user == message.author:
                        await self.embed.edit(embed=embed_green)
                        self.command_maker.remove(message.author.id)
                        await self.embed.clear_reactions()
                        embed_success=discord.Embed(description="[Go to Message](https://discordapp.com/channels/{}/{}/{})".format(message.guild.id, message.channel.id, message.id), color=0x43ff0d)
                        embed_success.set_author(name="{} found this tip helpful".format(message.author),icon_url=message.author.avatar_url)
                        embed_success.set_footer(text="TheNexusNation.com • {} {}".format(self.now.strftime("%d/%m/%Y"), self.now.strftime("%H:%M")))
                        await self.bot.get_channel(await self.config.logs_channel()).send(embed=embed_success)

                    elif str(reaction) == '<:cross:445640325780865035>' and user == message.author:
                        embed6 = discord.Embed(title="Please react accordingly", description=":one: - Did not fix my problem\n:two: - Was not a relevant response", color=0xff0000)
                        await self.embed.clear_reactions()
                        await self.embed.edit(embed=embed6)
                        
                        await self.embed.add_reaction(emoji = "1\N{combining enclosing keycap}")
                        await self.embed.add_reaction(emoji = "2\N{combining enclosing keycap}")
                        
                        def checkRedReaction(reaction, user):
                            return user == message.author and (str(reaction.emoji) == '1\N{combining enclosing keycap}' or str(reaction.emoji) == '2\N{combining enclosing keycap}')
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=900, check=checkRedReaction)
                            if str(reaction.emoji) == '1\N{combining enclosing keycap}' and user == message.author:

                                await self.embed.clear_reactions()
                                await self.embed.edit(embed=bad_reaction_one)
                                self.command_maker.remove(message.author.id)
                                value = "Did not fix my problem/answer my question"
                                embedBad=discord.Embed(description="[Go to Message](https://discordapp.com/channels/{}/{}/{})".format(message.guild.id, message.channel.id, message.id), color=0xff0000)
                                embedBad.set_author(name="{} did not find this tip helpful".format(message.author),icon_url=message.author.avatar_url)
                                embedBad.add_field(name="Reason", value=value, inline=True)
                                embedBad.add_field(name="Original Message", value=str(message.content), inline=False)
                                embedBad.set_footer(text="TheNexusNation.com • {} {}".format(self.now.strftime("%d/%m/%Y"), self.now.strftime("%H:%M")))
                                await self.bot.get_channel(await self.config.logs_channel()).send(embed=embedBad)
                                

                            elif str(reaction.emoji) == '2\N{combining enclosing keycap}' and user == message.author:
                                await self.embed.clear_reactions()
                                await self.embed.edit(embed=bad_reaction_two)
                                self.command_maker.remove(message.author.id)
                                value = "Response was not relevant"
                                embedBad=discord.Embed(description="[Go to Message](https://discordapp.com/channels/{}/{}/{})".format(message.guild.id, message.channel.id, message.id), color=0xfca503)
                                embedBad.set_author(name="{} did not find this tip helpful".format(message.author),icon_url=message.author.avatar_url)
                                embedBad.add_field(name="Reason", value=value, inline=True)
                                embedBad.add_field(name="Original Message", value=str(message.content), inline=False)
                                embedBad.set_footer(text="TheNexusNation.com • {} {}".format(self.now.strftime("%d/%m/%Y"), self.now.strftime("%H:%M")))
                                await self.bot.get_channel(await self.config.logs_channel()).send(embed=embedBad)

                        except asyncio.TimeoutError:
                            await self.embed.clear_reactions()
                            await self.embed.edit(embed=timed_out)
                            embed_timedout=discord.Embed(description="[Go to Message](https://discordapp.com/channels/{}/{}/{})".format(message.guild.id, message.channel.id, message.id))
                            embed_timedout.set_author(name="{} did not respond in time.".format(message.author),icon_url=message.author.avatar_url)
                            embed_timedout.add_field(name="Original Message", value=str(message.content), inline=False)
                            embed_timedout.set_footer(text="TheNexusNation.com • {} {}".format(self.now.strftime("%d/%m/%Y"), self.now.strftime("%H:%M")))
                            await self.bot.get_channel(await self.config.logs_channel()).send(embed=embed_timedout)
                            self.command_maker.clear()
                            pass
                except asyncio.TimeoutError:
                    await self.embed.clear_reactions()
                    await self.embed.edit(embed=timed_out)
                    embed_timedout=discord.Embed(description="[Go to Message](https://discordapp.com/channels/{}/{}/{})".format(message.guild.id, message.channel.id, message.id))
                    embed_timedout.set_author(name="{} did not respond in time.".format(message.author),icon_url=message.author.avatar_url)
                    embed_timedout.add_field(name="Original Message", value=str(message.content), inline=False)
                    embed_timedout.set_footer(text="TheNexusNation.com • {} {}".format(self.now.strftime("%d/%m/%Y"), self.now.strftime("%H:%M")))
                    await self.bot.get_channel(await self.config.logs_channel()).send(embed=embed_timedout)
                    self.command_maker.clear()
                    pass
