import discord, datetime, asyncio, aiohttp, decimal
from redbot.core import commands, checks, Config
import mysql.connector
from mysql.connector import Error

def communityid_converter(communityid):
    steamid64ident = 76561197960265728
    sid_split = communityid.split(':')
    commid = int(sid_split[2]) * 2
    if sid_split[1] == '1':
        commid += 1
    commid += steamid64ident
    return commid

async def gangEmbed(ctx, gangs, name, index):
    gang_data, positions, kills, names = {}, [], [], []

    for k, v in enumerate(gangs):
        gang_data.update({f"{k+1}": {"name": v[1], "kills": v[index]}})
    embed = discord.Embed(
        timestamp = datetime.datetime.utcnow(),
        colour=0xff0000
    )
    embed.set_author(
        name=f"Top Jailbreak {name}",
        icon_url="https://cdn.discordapp.com/icons/269912749327253504/08d4ddc1e97d0314de83196806bb1f9c.webp?size=128"
    )
    for i in gang_data:
        positions.append(i)
        names.append(gang_data[i].get("name"))
        kills.append(str(gang_data[i].get("kills")))
    embed.add_field(
        name="Pos",
        value="\n".join(positions)
    )
    embed.add_field(
        name="Name",
        value="\n".join(names)
    )
    embed.add_field(
        name="Kills",
        value="\n".join(kills)
    )
    await ctx.send(embed=embed)

async def leaderboardEmbed(ctx, players, name):
    data, positions, names, wins = {}, [], [], []
    for k, v in enumerate(players):
        data.update({f"{k+1}": {"name": v[0], "wins": v[1]+v[2]+v[3]+v[4]}})
    embed = discord.Embed(
        timestamp = datetime.datetime.utcnow(),
        colour=0xff0000
    )
    embed.set_author(
        name=f"Top {name} Players",
        icon_url="https://cdn.discordapp.com/icons/269912749327253504/08d4ddc1e97d0314de83196806bb1f9c.webp?size=128"
    )
    for i in data:
        positions.append(i)
        names.append(data[i].get("name"))
        wins.append(str(data[i].get("wins")))
    embed.add_field(
        name="Pos",
        value="\n".join(positions)
    )
    embed.add_field(
        name="Name",
        value="\n".join(names)
    )
    embed.add_field(
        name="Wins",
        value="\n".join(wins)
    )
    await ctx.send(embed=embed)

async def tttStats(ctx, stats, member):
    embed = discord.Embed(
        timestamp = datetime.datetime.utcnow(), 
        colour=0xff0000
    )
    embed.set_author(
        name=f"{member} TTT Stats",
        icon_url="https://cdn.discordapp.com/icons/269912749327253504/08d4ddc1e97d0314de83196806bb1f9c.webp?size=128"
    )
    embed.add_field(
        name="Rounds Played",
        value=stats[0]
    )
    embed.add_field(
        name="Rounds Won",
        value=stats[1]
    )
    embed.add_field(
        name="Shots Fired",
        value=stats[2]
    )
    embed.add_field(
        name="Damage Dealt",
        value=stats[3]
    )
    embed.add_field(
        name="Damage Taken",
        value=stats[4]
    )
    embed.add_field(
        name="Innocents Killed",
        value=stats[5]
    )
    embed.add_field(
        name="Traitors Killed",
        value=stats[6]
    )
    embed.add_field(
        name="Detectives Killed",
        value=stats[7]
    )
    embed.add_field(
        name="Tased Traitors",
        value=stats[8]
    )
    await ctx.send(embed=embed)

async def surfbhopStats(ctx, stats, member):
    points = stats[0]
    wrpoints = stats[1]
    top10points = stats[2]
    finishedmapspro = stats[3]
    finishedbonuses = stats[4]
    finishedstages = stats[5]
    wrs = stats[6]
    wrbs = stats[7]
    wrcps = stats[8]
    top10s = stats[9]
    lastseen = datetime.datetime.fromtimestamp(int(stats[10])).strftime('%d-%m-%Y @ %H:%M:%S')
    joined = datetime.datetime.fromtimestamp(int(stats[11])).strftime('%d-%m-%Y @ %H:%M:%S')
    timealive = datetime.timedelta(seconds=stats[13])
    connections = stats[13]
    country = stats[14]
    country = country.replace("The ","")
    style = stats[15]
    styles = ["Normal", "Sideways", "Half-Sideways", "Backwards", "Low-Gravity", "Slow Motion", "Fast Forward", "Freestyle"]    

    if wrpoints > 0:
        top10string = f"{top10s} - [{top10points}+{wrpoints}]"
    else:
        top10string = f"{top10s} - [{top10points}]"
    
    embed = discord.Embed(
        timestamp = datetime.datetime.utcnow(),
        colour=0xff0000
    )
    embed.set_author(
        name=f"{member} {styles[style]} Surf Stats",
        icon_url="https://cdn.discordapp.com/icons/269912749327253504/08d4ddc1e97d0314de83196806bb1f9c.webp?size=128"
    )
    embed.add_field(
        name="Total Points",
        value=points
    )
    embed.add_field(
        name="Top 10 Records",
        value=top10string
    )
    embed.add_field(
        name="Country",
        value=country
    )
    embed.add_field(
        name="First Joined",
        value=joined
    )
    embed.add_field(
        name="Last Online",
        value=lastseen
    )
    embed.add_field(
        name="Time Played",
        value=timealive
    )
    embed.add_field(
        name="Records",
        value=f"Map WR: {wrs}\nStage WR: {wrcps}\nBonus WR: {wrbs}"
    )
    embed.add_field(
        name="Completed",
        value=f"Maps: {finishedmapspro}\nStages: {finishedstages}\nBonuses: {finishedbonuses}"
    )
    embed.add_field(
        name="Total Connections",
        value=connections
    )
    await ctx.send(embed=embed)

class QueryTNN(commands.Cog):
    __author__ = "Raff"
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.pwd = ""

    @commands.group(name="jb")
    async def jailbreak_commands(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @jailbreak_commands.command()
    async def players(self, ctx):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='jailbreak',
                user='webserver',
                password=self.pwd)
            if connection.is_connected():
                names = []
                cursor = connection.cursor()
                cursor.execute(f"SELECT `player`, `guard`, `prisoner`, `special`, `lastrequest` FROM `jailbreak_stats` ORDER BY `guard` + `prisoner` + `special` + `lastrequest` DESC LIMIT 10;")
                result = cursor.fetchall()
                await leaderboardEmbed(ctx, result, "Jailbreak")

        except Error as e:
            print("Error while connecting to MySQL", e)

    @jailbreak_commands.command()
    async def gangs(self, ctx):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='jailbreak',
                user='webserver',
                password=self.pwd)
            if connection.is_connected():
                names = []
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM `gangs_groups` ORDER BY `kills` DESC LIMIT 10;")
                result = cursor.fetchall()

                await gangEmbed(ctx, result, "Gangs", 10)

        except Error as e:
            print("Error while connecting to MySQL", e)

    @jailbreak_commands.command()
    async def squads(self, ctx):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='jailbreak',
                user='webserver',
                password=self.pwd)
            if connection.is_connected():
                names = []
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM `squad_groups` ORDER BY `kills` DESC LIMIT 10;")
                result = cursor.fetchall()

                await gangEmbed(ctx, result, "Squads", 11)

        except Error as e:
            print("Error while connecting to MySQL", e)


    @commands.group(name="ttt")
    async def ttt_commands(self, ctx):
        if ctx.invoked_subcommand is None:
            pass
    
    @ttt_commands.command()
    async def stats(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='discord_integration',
                user='webserver',
                password=self.pwd)
            if connection.is_connected():
                names = []
                cursor = connection.cursor()
                try:
                    cursor.execute(f"SELECT `steamid` FROM `du_users` WHERE userid = '{member.id}';")
                    result = cursor.fetchone()
                    community_id = communityid_converter(result[0])
                    cursor.execute(f"SELECT rounds_played, rounds_won, shots_fired, damage_given, damage_taken, killed_innocents, killed_traitors, killed_detectives, scanned_traitors FROM `ttt`.`ttt_stats` WHERE communityid = '{community_id}';")
                    result = cursor.fetchone()
                    await tttStats(ctx, result, member)
                except Exception as e:
                    await ctx.send(f"> TTT stats for {member.mention} not found.")



        except Error as e:
            print("Error while connecting to MySQL", e)

    @commands.group(name="surf")
    async def surf_commands(self, ctx):
        if ctx.invoked_subcommand is None:
            pass
    
    @surf_commands.command()
    async def stats(self, ctx, style = None, member: discord.Member = None):
        if member is None:
            member = ctx.author
        if style is None:
            prefix = ctx.prefix
            await ctx.send(f"> No style specified, please use ``n``, ``sw``, ``hsw``, ``bw``, ``lg``, ``sm``, ``ff``, ``fs``.\n> Example: ``{prefix}surf stats hsw``.")
            return
        if style == "n":
            styleint = 0
        if style == "sw":
            styleint = 1
        if style == "hsw":
            styleint = 2
        if style == "bw":
            styleint = 3
        if style == "lg":
            styleint = 4
        if style == "sm":
            styleint = 5
        if style == "ff":
            styleint = 6
        if style == "fs":
            styleint = 7
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='discord_integration',
                user='webserver',
                password=self.pwd)
            if connection.is_connected():
                names = []
                cursor = connection.cursor()
                try:
                    cursor.execute(f"SELECT `steamid` FROM `du_users` WHERE userid = '{member.id}';")
                    result = cursor.fetchone()
                    community_id = result[0]
                    cursor.execute(f"SELECT points, wrpoints, top10points, finishedmapspro, finishedbonuses, finishedstages, wrs, wrbs, wrcps, top10s, lastseen, joined, timealive, connections, country, style FROM `surf`.`ck_playerrank` WHERE steamid = '{community_id}' AND style = {styleint};")
                    result = cursor.fetchone()
                    await surfbhopStats(ctx, result, member)
                except Exception as e:
                    await ctx.send(f"> Surf stats for {member.mention} not found.")

        except Error as e:
            print("Error while connecting to MySQL", e)

    @commands.group(name="bhop")
    async def bhop_commands(self, ctx):
        if ctx.invoked_subcommand is None:
            pass
    
    @bhop_commands.command()
    async def stats(self, ctx, style = None, member: discord.Member = None):
        if member is None:
            member = ctx.author
        if style is None:
            prefix = ctx.prefix
            await ctx.send(f"> No style specified, please use ``n``, ``sw``, ``hsw``, ``bw``, ``lg``, ``sm``, ``ff``, ``fs``.\n> Example: ``{prefix}bhop stats hsw``.")
            return
        if style == "n":
            styleint = 0
        if style == "sw":
            styleint = 1
        if style == "hsw":
            styleint = 2
        if style == "bw":
            styleint = 3
        if style == "lg":
            styleint = 4
        if style == "sm":
            styleint = 5
        if style == "ff":
            styleint = 6
        if style == "fs":
            styleint = 7
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='discord_integration',
                user='webserver',
                password=self.pwd)
            if connection.is_connected():
                names = []
                cursor = connection.cursor()
                try:
                    cursor.execute(f"SELECT `steamid` FROM `du_users` WHERE userid = '{member.id}';")
                    result = cursor.fetchone()
                    community_id = result[0]
                    cursor.execute(f"SELECT points, wrpoints, top10points, finishedmapspro, finishedbonuses, finishedstages, wrs, wrbs, wrcps, top10s, lastseen, joined, timealive, connections, country, style FROM `bhop`.`ck_playerrank` WHERE steamid = '{community_id}' AND style = {styleint};")
                    result = cursor.fetchone()
                    await surfbhopStats(ctx, result, member)
                except Exception as e:
                    await ctx.send(f"> Bhop stats for {member.mention} not found.")

        except Error as e:
            print("Error while connecting to MySQL", e)