import discord, datetime, asyncio, aiohttp, decimal
from redbot.core import commands, checks, Config
import mysql.connector
from mysql.connector import Error


async def pickCharacter(ctx, characters, member):

    emojis = [
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
        "5️⃣",
        "6️⃣",
        "7️⃣",
        "8️⃣",
        "9️⃣"
    ]

    character_names = []
    character_ids = []
    for i, v in enumerate(characters):
        character_names.append(str(i+1)+" - "+characters[i][1]+" "+characters[i][2])
        character_ids.append(characters[i][0])

    embed = discord.Embed(
        description=f"**{ctx.author}** has said that you referred them to the city! Because of this we are giving you **$1000** as a reward. Please choose a character from the list below by reacting to their respective number.\n**Do not be in the city at the time of completing this process as you will NOT receive your reward.**",
        timestamp=datetime.datetime.utcnow(),
        color=0x2a9946
    )
    embed.set_author(
        name="Nexus Roleplay Referrals",
        icon_url=ctx.author.avatar_url
    )
    embed.add_field(
        name="Your Characters",
        value="\n".join(character_names)
    )
    try:
        char_message = await ctx.send(embed=embed)
    except:
        await ctx.send("User has their DMs closed.")
    for i, character in enumerate(characters):
        await char_message.add_reaction(emojis[i])

async def referredLog(ctx, member):
    try:
        logs_channel = discord.utils.get(ctx.guild.text_channels, id=746474884133027851)
    except:
        print("Could not find RAF logs channel")
    else:
        embed = discord.Embed(
            title="Recruit a Friend Logs",
            color=0x2a9946,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(
            name="Referrer",
            value=member.mention
        )
        embed.add_field(
            name="Referee",
            value=ctx.author.mention
        )
        embed.add_field(
            name="Award",
            value="$1000"
        )
        await logs_channel.send(embed=embed)


class Querynrp(commands.Cog):
    __author__ = "Raff"
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=12345678)
        default_guild = {
            "blacklisted_steam": []
        }
        self.config.register_guild(**default_guild)

    @commands.guild_only()
    @commands.command()
    async def referrer(self, ctx, member: discord.Member):
        if ctx.author != member:
            pwd = "bZsB+XSK1@8A3nb-"
            try:
                connection = mysql.connector.connect(host='localhost',
                                                    database='nexusrp',
                                                    user='nrp',
                                                    password=f'{pwd}')
                if connection.is_connected():

                    online = []
                    referrer_discord_id = member.id
                    referee_discord_id = ctx.author.id
                    cursor = connection.cursor()
                    try:
                        cursor.execute(f"SELECT SUM(playtime) FROM characters INNER JOIN users ON characters.identifier = users.identifier WHERE isDeleted = 0 AND discord = 'discord:{referee_discord_id}'")
                        playtime = cursor.fetchone()
                    except:
                        await ctx.send("Could not find character")
                    else:
                        if isinstance(playtime[0], decimal.Decimal):
                            if (playtime[0]>600) and (playtime[0]<1200):

                                emojis = [
                                    "1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"
                                ]

                                def check(reaction, user):
                                    return (user == member) and (str(reaction.emoji) in emojis)

                                def findCharacter(reaction):
                                    for i, emoji in enumerate(emojis):
                                        if str(emoji) == str(reaction):
                                            return i
                                        else:
                                            continue
                                    return false

                                

                                cursor = connection.cursor()
                                cursor.execute(f"SELECT characters.id, firstname, lastname FROM characters INNER JOIN users ON characters.identifier = users.identifier WHERE isDeleted = 0 AND discord = 'discord:{referrer_discord_id}'")
                                characters = cursor.fetchall()
                                cursor.execute(f"SELECT identifier FROM users WHERE discord = 'discord:{referee_discord_id}'")
                                referee_steam_id = cursor.fetchone()
                                print(characters)
                                if characters:
                                    async with self.config.guild(ctx.guild).blacklisted_steam() as blacklisted:
                                        if referee_steam_id[0] not in blacklisted:
                                            for i in blacklisted:
                                                await ctx.send(i)
                                            await ctx.send("your id"+referee_steam_id[0])
                                            await pickCharacter(ctx, characters, member)
                                            try:
                                                reaction, user = await self.bot.wait_for('reaction_add', timeout = 300, check = check)
                                            except asyncio.TimeoutError:
                                                try:
                                                    await member.send("You ran out of time to pick a character.")
                                                except:
                                                    pass
                                            else:
                                                await member.send(f"**$1000** has been added to your character: `{characters[findCharacter(reaction)][1]} {characters[findCharacter(reaction)][2]}`")
                                                character_number = int(characters[findCharacter(reaction)][0])
                                                cursor.execute(f"UPDATE characters SET money = money + 1000 WHERE id = {character_number}")
                                                cursor.execute(f"SELECT identifier FROM characters WHERE id = {character_number}")
                                                blid = cursor.fetchone()
                                                blacklisted.append(blid[0])
                                                print(f"BLACKLISTED `{blid[0]}`")
                                                await referredLog(ctx, member)
                                        else:
                                            await ctx.send("You have already been referred by someone else.")
                                else:
                                    await ctx.send(f"{member.mention} has not launched the Discord Client and FiveM together, or does not have any characters created on Nexus Roleplay.")

                            elif playtime[0]<600:
                                await ctx.send("You need to have at least **10 hours** of playtime on one character to qualify for this.")
                            elif playtime[0]>1200:
                                await ctx.send("You no longer qualify for the recruit a friend system due to exceeding the threshold of **20 hours** of playtime.")

                        else:
                            await ctx.send(f"{ctx.author.mention} You either have not launched the Discord Client and FiveM together, or have no character created on Nexus Roleplay.")
                        

            except Error as e:
                print("Error while connecting to MySQL", e)
        else:
            await ctx.send("You cannot refer yourself.")





    @commands.guild_only()
    @commands.has_any_role(713167412735770635, 713166994471518269, 699702705123491990, 713167480339562527)
    @commands.command(name="pnumber")
    async def change_phone_number(self, ctx, character_id, phone_number):
        if len(phone_number) == 7:
            pwd = "bZsB+XSK1@8A3nb-"
            try:
                connection = mysql.connector.connect(host='localhost',
                                                    database='nexusrp',
                                                    user='nrp',
                                                    password=f'{pwd}')
                if connection.is_connected():
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT * FROM characters WHERE phone_number = {phone_number}")
                    phone_dupe_check = cursor.fetchall()
                    if phone_dupe_check is None:
                        cursor.execute(f"UPDATE characters SET phone_number = {phone_number} WHERE id = {character_id}")
                        cursor.execute(f"SELECT firstname, lastname FROM characters WHERE id = {character_id}")
                        character_name = cursor.fetchone()
                        try:
                            messg = await ctx.send(f"Changed **{character_name[0]} {character_name[1]}** phone number to: `{phone_number}`")
                        except:
                            await ctx.send(f"Character does not exist.")
                        else:
                            await messg.add_reaction("✅")
                    else:
                        await ctx.send("There is already a character with this phone number.")
                    
                    

            except Error as e:
                print("Error while connecting to MySQL", e)
        else:
            await ctx.send("Phone numbers must be `7` characters long.")

    @commands.guild_only()
    @commands.command()
    async def characters(self, ctx, member: discord.Member):
        pwd = "bZsB+XSK1@8A3nb-"
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='nexusrp',
                user='nrp',
                password=f'{pwd}')
            if connection.is_connected():
                names = []
                cursor = connection.cursor()
                cursor.execute(f"SELECT firstname, lastname, characters.id FROM characters INNER JOIN users ON characters.identifier = users.identifier WHERE isDeleted = 0 AND discord = 'discord:{member.id}'")
                characters = cursor.fetchall()
                for i, character in enumerate(characters):
                    names.append(str(characters[i][0])+" "+str(characters[i][1])+" - "+str(characters[i][2]))
                embed = discord.Embed(
                    title="Your Characters",
                    description="\n".join(names),
                    timestamp=datetime.datetime.now(),
                    color=0x2a9946
                )
                await ctx.send(embed=embed)

        except Error as e:
            print("Error while connecting to MySQL", e)


    @commands.guild_only()
    @commands.has_any_role(713167412735770635, 713166994471518269, 699702705123491990, 713167480339562527)
    @commands.command()
    async def online(self, ctx):
        pwd = "bZsB+XSK1@8A3nb-"
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='nexusrp',
                user='nrp',
                password=f'{pwd}')
            if connection.is_connected():
                names = []
                cursor = connection.cursor()
                cursor.execute(f"SELECT name, character_name, current_id FROM users WHERE isOnline = 1")
                players = cursor.fetchall()
                for i, character in enumerate(players):
                    names.append(str("**"++str(character[2])+"**"+" - "+"**"+character[0]+"**")+" - "+str(character[1]))
                embed = discord.Embed(
                    title="Online Players",
                    description="\n".join(names),
                    timestamp=datetime.datetime.now(),
                    color=0x2a9946
                )
                await ctx.send(embed=embed)

        except Error as e:
            print("Error while connecting to MySQL", e)