import discord, datetime, asyncio, aiohttp, random
from redbot.core import commands, checks, Config

async def send_crate(ctx, items, price):

    crate = discord.Embed(
        color = 0x2a9946,
        timestamp = datetime.datetime.now()
    )
    crate.add_field(
        name="Items",
        value= "\n".join(items),
        inline=False
    )
    crate.add_field(
        name="Estimated Price",
        value=f"${price}",
        inline=False
    )
    crate.set_author(
        name="Weapons Container"
    )
    crate.set_footer(
        text = "Copyright © 2020 NexusHub.io",
        icon_url = "https://cdn.discordapp.com/icons/699702073951912028/a_1d960abbbe922ff536e0d469dc4f518a.webp?size=128"
    )
    try:
        await ctx.author.send(embed=crate)
        log_channel = discord.utils.get(ctx.guild.text_channels, id=741278281575170098)
        await log_channel.send(content=f"{ctx.author.mention} rolled a crate",embed=crate)
    except:
        pass
    else:
        await ctx.message.add_reaction("✅")

class Bidding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=6942069)
        default_guild = {
            "weapons": [
                ["Handcuffs",12500, 250],
                ["Handcuffs",12500, 250],
                ["Battleaxe",7000, 246],
                ["Battleaxe",7000, 246],
                ["Battleaxe",7000, 246],
                ["Switchblade",7000, 201],
                ["Switchblade",7000, 201],
                ["Switchblade",7000, 201],
                ["Handcuffs",12500, 250],
                ["Handcuffs",12500, 250],
                ["Heavy Pistol",4500, 234],
                ["Heavy Pistol",4500, 234],
                ["Heavy Pistol",4500, 234],
                ["Heavy Pistol",4500, 234],
                ["Revolver",10000, 243],
                ["Revolver",10000, 243],
                ["Revolver",10000, 243],
                ["Revolver",10000, 243],
                ["Desert Eagle",10000, 219],
                ["Desert Eagle",10000, 219],
                ["Desert Eagle",10000, 219],
                ["Desert Eagle",10000, 219],
                ["AP Pistol",20000, 218],
                ["AP Pistol",20000, 218],
                ["AP Pistol",20000, 218],
                ["TEC-9",20000, 242],
                ["TEC-9",20000, 242],
                ["TEC-9",20000, 242],
                ["Scorpion",25000, 190],
                ["Scorpion",25000, 190],
                ["Scorpion",25000, 190],                
                ["Mini UZI",30000, 190],
                ["Mini UZI",30000, 190],
                ["Mini UZI",30000, 190],
                ["MP5",32500, 220],        
                ["MP5",32500, 220],
                ["MP5",32500, 220],
                ["Tommy Gun",45000, 209],
                ["Tommy Gun",45000, 209],
                ["Tommy Gun",45000, 209],
                ["Pump Shotgun",45000, 199],
                ["Pump Shotgun",45000, 199],
                ["Pump Shotgun",45000, 199],
                ["Assault Shotgun",50000, 226],
                ["Assault Shotgun",50000, 226],
                ["Compact Rifle",70000, 244],
                ["Compact Rifle",70000, 244],
                ["Bullpump Rifle",75000, 235],
                ["Special Carbine",80000, 233],
                ["Carbine Rifle",90000, 222],
                ["AK-47",100000, 171],                
                ["Combat MG",140000, 225],   
                ["MG",160000, 224],   
                ["Suppressor",2000, 170],   
                ["Human Fixkit",450, 73],   
                ["Human Fixkit",450, 73],   
                ["Emergency Medkit",1000, 145],   
                ["Emergency Medkit",1000, 145],   
                ["Blindfold",1000, 76],   
                ["Blindfold",1000, 76],   
                ["Blindfold",1000, 76],   
                ["Suppressor",2000, 170],   
                ["Suppressor",2000, 170],   
                ["Suppressor",2000, 170],   
                ["Advanced Lockpick",3000, 21],   
                ["Blank Plate",15000, 262],
                ["Bulletproof Vest", 1500, 42],  
                ["Bulletproof Vest", 1500, 42],
                ["Bulletproof Vest", 1500, 42]                                                
            ]
        }
        self.config.register_guild(**default_guild)


    @commands.has_any_role("Server Admin","Lead Admin","Community Manager", "Owner")
    @commands.guild_only()
    @commands.command()
    async def crate(self, ctx):
        items = []
        total_price = 0
        items_to_pick = random.randrange(4,10)
        async with self.config.guild(ctx.guild).weapons() as weapons:
            for i in range(items_to_pick):
                pick = random.randrange(0, 68)
                items.append(f"{weapons[pick][0]} - {weapons[pick][2]}")
                total_price += weapons[pick][1]
        try:
            await send_crate(ctx, items, total_price)
        except:
            await ctx.send("> Failed to send crate")
        
