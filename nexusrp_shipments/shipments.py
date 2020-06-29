import discord, datetime, asyncio, aiohttp, random
from redbot.core import commands, checks, Config

async def ship_package(ctx, color, tier, collection_items, collection_price, collection_name, user):

    await user.send("**3...**")
    await asyncio.sleep(1)
    await user.send("**2...**")
    await asyncio.sleep(1)
    await user.send("**1...**")
    await asyncio.sleep(1)

    shipment = discord.Embed(
        color = color,
        timestamp = datetime.datetime.now()
    )
    shipment.add_field(
        name="Collection Name",
        value=collection_name,
        inline=False
    )
    shipment.add_field(
        name="Items",
        value= "\n".join(collection_items),
        inline=False
    )
    shipment.add_field(
        name="Total Worth",
        value=collection_price,
        inline=False
    )
    shipment.set_author(
        name=tier + " Shipment"
    )
    shipment.set_footer(
        text = "Copyright © 2020 NexusHub.io",
        icon_url = "https://cdn.discordapp.com/icons/699702073951912028/a_1d960abbbe922ff536e0d469dc4f518a.webp?size=128"
    )
    try:
        await user.send(content = f"{user.mention} Here is the shipment you will receive. Contact `💎tiggs#0001` to receive your shipment.", embed = shipment)
    except discord.errors.Forbidden:
        await ctx.send(f">>> {member.mention} has their DMs closed.")
    else:
        await ctx.author.send(content = f"{ctx.author.mention} This the Gun Shipment for {user.mention}", embed = shipment)
    

async def terms_of_service(ctx, color, tier, collection_items, collection_price, collection_name, user):

    def check(reaction, reactor):
        return (reactor == user) and (tos.channel == reaction.message.channel) and (str(reaction.emoji) == "✅")

    terms = discord.Embed(
        description = "By accepting this agreement, you agree that you have a current balance of at least $150,000 and agree that upon accepting this agreement, $150,000 will be removed from you and will be reflected in your ``/cash`` balance.\n\nYou agree that the shipment you receive is final and is awarded to you based on a fair system, completely automated by our <@!409819492655562767> bot. You agree that the shipment of guns will be delivered within 24 hours, and instant delivery is not promised. You also agree that once the shipment is in your possession the government takes no responsibility regarding your shipment.\n\n**React to the ✅ below to accept these terms and receive your shipment.**",
        color = 0x2a9946,
        timestamp = datetime.datetime.now()
    )
    terms.set_author(
        name="Gun Shipment Terms of Service"
    )
    terms.set_footer(
        text = "Copyright © 2020 NexusHub.io",
        icon_url = "https://cdn.discordapp.com/icons/699702073951912028/a_1d960abbbe922ff536e0d469dc4f518a.webp?size=128"
    )
    try:
        tos = await user.send(embed=terms)
    except discord.errors.Forbidden:
        await ctx.send(f">>> {member.mention} has their DMs closed.")
    else:
        await tos.add_reaction("✅")

        try:

            reaction, reactor = await ctx.cog.bot.wait_for('reaction_add', check=check,timeout=300)

        except asyncio.TimeoutError:

            await user.send(">>> You did not react in time to our Terms of Service and your order has been cancelled.")
        
        else:

            await ship_package(ctx, color, tier, collection_items, collection_price, collection_name, user)

class Shipments(commands.Cog):

    __author__ = "Raff"
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=696969)
        default_guild = {
            "packages": [
                [
                    [
                        ["Handcuffs","Handcuff Key","Heavy Pistol","Scorpion","Mini Uzi"],
                        "$107,500",
                        "The Handcuff Collection"
                        ],
                    [
                        ["Revolver","Switchblade","Switchblade","Tec9","Tec9","Mini Uzi"],
                        "$114,000",
                        "The Small Weapons Collection"
                        ],
                    [
                        ["Heavy Pistol","Heavy Pistol","Heavy Pistol","Revolver","Revolver","Revolver","Battleaxe","Battleaxe","Switchblade","Switchblade","Desert Eagle","Desert Eagle"],
                        "$116,000",
                        "The Melee Collection"
                        ],
                    [
                        ["Heavy Pistol","Heavy Pistol","Revolver","Revolver","Battleaxe","Mini AK-47"],
                        "$108,000",
                        "The Rifle Collection"
                        ],
                    [
                        ["Heavy Pistol","Revolver","Battleaxe","Battleaxe","Switchblade","Tec9","Tec9","Scorpion"],
                        "$118,500",
                        "The SMG Collection"
                        ],
                    [
                        ["Revolver","Revolver","Battleaxe","Desert Eagle","Desert Eagle","Desert Eagle","Desert Eagle","Scorpion"],
                        "$117,500",
                        "The Small Weapons 2 Collection"
                        ],
                    [
                        ["Heavy Pistol","Heavy Pistol","Heavy Pistol","Heavy Pistol","Heavy Pistol","Revolver","Revolver","Revolver","Desert Eagle","Desert Eagle","Desert Eagle","Tec9"],
                        "$117,000",
                        "The Handgun Collection"
                        ]
                    ], # 40% 0 - 40
                [
                    [
                        ["Handcuffs","Handcuff Key","Heavy Pistol","Scorpion","Scorpion","Assault Shotgun"],
                        "$146,000",
                        "The Handcuff Collection"
                        ],
                    [
                        ["Revolver","Switchblade","Tec9","Heavy Pistol","Special Carbine"],
                        "$124,500",
                        "The Small Weapons Collection"
                        ],
                    [
                        ["Heavy Pistol","Revolver","Battleaxe","Battleaxe","Switchblade","Switchblade","Desert Eagle","Scorpion","Scorpion"],
                        "$124,500",
                        "The Melee Collection"
                        ],
                    [
                        ["Revolver","Switchblade","Scorpion","Special Carbine"],
                        "$123,000",
                        "The Rifle Collection"
                        ],
                    [
                        ["Revolver","Desert Eagle","MP5","Mini Uzi"],
                        "$125,000",
                        "The SMG Collection"
                        ],
                    [
                        ["Revolver","Revolver","Revolver","Battleaxe","Desert Eagle","Tec9","Tec9","AP Pistol"],
                        "$129,000",
                        "The Small Weapons 2 Collection"
                        ],
                    [
                        ["Heavy Pistol","Heavy Pistol","Revolver","Revolver","Revolver","Revolver","Revolver","Desert Eagle","Desert Eagle","Desert Eagle","AP Pistol"],
                        "$123,000",
                        "The Handgun Collection"
                        ]
                    ], # 20% 41 - 61
                [
                    [
                        ["Handcuffs","Handcuff Key","Switchblade","Scorpion","Scorpion","Mini AK-47"],
                        "$170,500",
                        "The Handcuff Collection"
                        ],
                    [
                        ["Revolver","Switchblade","Tec9","Tec9","AP Pistol","MP5"],
                        "$164,000",
                        "The Small Weapons Collection"
                        ],
                    [
                        ["Heavy Pistol","Revolver","Revolver","Battleaxe","Battleaxe","Switchblade","Switchblade","Desert Eagle","Desert Eagle","Desert Eagle","Scorpion","Scorpion"],
                        "$164,500",
                        "The Melee Collection"
                        ],
                    [
                        ["Desert Eagle","Tommy Gun","Special Carbine"],
                        "$166,000",
                        "The Rifle Collection"
                        ],
                    [
                        ["Heavy Pistol","Heavy Pistol","Revolver","Switchblade","Scorpion","Scorpion","Mini Uzi","Tommy Gun"],
                        "$170,000",
                        "The SMG Collection"
                        ],
                    [
                        ["Heavy Pistol","Heavy Pistol","Heavy Pistol","Revolver","Switchblade","Switchblade","Battleaxe","Desert Eagle","Desert Eagle","Mini Uzi","Tommy Gun"],
                        "$175,000",
                        "The Small Weapons 2 Collection"
                        ],
                    [
                        ["Heavy Pistol","Revolver","Revolver","Revolver","Desert Eagle","Desert Eagle","Desert Eagle","AP Pistol","AP Pistol","AP Pistol"],
                        "$169,500",
                        "The Handgun Collection"
                        ]
                    ], # 15% 62 - 77
                [
                    [
                        ["Handcuffs","Handcuff Key","Heavy Pistol","Scorpion","Scorpion","Mini Uzi","MP5"],
                        "$201,000",
                        "The Handcuff Collection"
                        ],
                    [
                        ["Revolver","Switchblade","Tec9","Tec9","Tec9","Desert Eagle","Desert Eagle","Bullpump Rifle"],
                        "$204,000",
                        "The Small Weapons Collection"
                        ],
                    [
                        ["Heavy Pistol","Revolver","Revolver","Revolver","Battleaxe","Battleaxe","Switchblade","Switchblade","Handcuffs","Handcuff Key","Tec9","Tec9","Assault Shotgun"],
                        "$199,500",
                        "The Melee Collection"
                        ],
                    [
                        ["Heavy Pistol","Heavy Pistol","Revolver","AK-47","Tommy Gun"],
                        "$182,500",
                        "The Rifle Collection"
                        ],
                    [
                        ["Heavy Pistol","Heavy Pistol","Tec9","Tec9","Tec9","Tec9","Tec9","MP5"],
                        "$201,000",
                        "The SMG Collection"
                        ],
                    [
                        ["Revolver","Battleaxe","Desert Eagle","Desert Eagle","Mini Uzi","AK-47"],
                        "$191,500",
                        "The Small Weapons 2 Collection"
                        ],
                    [
                        ["Revolver","Revolver","Desert Eagle","Desert Eagle","Desert Eagle","AP Pistol","AP Pistol","AP Pistol","AP Pistol"],
                        "$190,500",
                        "The Handgun Collection"
                        ]
                    ], # 10% 78 - 88
                [
                    [
                        ["Handcuffs","Handcuff Key","Heavy Pistol","Switchblade","Switchblade","Switchblade","Combat MG"],
                        "$222,000",
                        "The Handcuff Collection"
                        ],
                    [
                        ["Revolver","Switchblade","Battleaxe","Tec9","Tec9","Assault Shotgun","AK-47"],
                        "$229,500",
                        "The Small Weapons Collection"
                        ],
                    [
                        ["Heavy Pistol","Heavy Pistol","Heavy Pistol","Heavy Pistol","Revolver","Revolver","Revolver","Battleaxe","Battleaxe","Switchblade","Switchblade","Scorpion","Scorpion","Carbine Rifle"],
                        "$226,500",
                        "The Melee Collection"
                        ],
                    [
                        ["Battleaxe","Switchblade","Switchblade","Scorpion","Assault Shotgun","AK-47"],
                        "$210,500",
                        "The Rifle Collection"
                        ],
                    [
                        ["Heavy Pistol","Revolver","Revolver","Switchblade","Desert Eagle","Tec9","Scorpion","Mini Uzi","MP5"],
                        "$221,000",
                        "The SMG Collection"
                        ],
                    [
                        ["Revolver","Battleaxe","Battleaxe","Desert Eagle","Desert Eagle","Scorpion","Scorpion","AP Pistol","AP Pistol","Mini Uzi"],
                        "$217,500",
                        "The Small Weapons 2 Collection"
                        ],
                    [
                        ["Revolver","Desert Eagle","Desert Eagle","Desert Eagle","Desert Eagle","Desert Eagle","Desert Eagle","AP Pistol","AP Pistol","AP Pistol","Scorpion"],
                        "$213,500",
                        "The Handgun Collection"
                        ]
                    ], # 4% 89-93
                [
                    [
                        ["Handcuffs","Handcuff Key","Heavy Pistol","Scorpion","Scorpion","MG"],
                        "$279,000",
                        "The Handcuff Collection"
                        ],
                    [
                        ["Heavy Pistol","Revolver","Switchblade","Tec9","Tec9","Desert Eagle","AP Pistol","Special Carbine","Bullpump Rifle"],
                        "$276,500",
                        "The Small Weapons Collection"
                        ],
                    [
                        ["Battleaxe","Battleaxe","Switchblade","Switchblade","Switchblade","AP Pistol","MG"],
                        "$262,000",
                        "The Melee Collection"
                        ],
                    [
                        ["Desert Eagle","Tec9","Tommy Gun","Special Carbine","Special Carbine"],
                        "$253,000",
                        "The Rifle Collection"
                        ],
                    [
                        ["Heavy Pistol","Heavy Pistol","Heavy Pistol","Revolver","Revolver","Revolver","Revolver","Switchblade","Scorpion","Scorpion","Scorpion","Mini Uzi","AK-47"],
                        "$277,000",
                        "The SMG Collection"
                        ],
                    [
                        ["Revolver","Revolver","Battleaxe","Battleaxe","Desert Eagle","Desert Eagle","Desert Eagle","AP Pistol","Bullpump Rifle","Bullpump Rifle"],
                        "$270,500",
                        "The Small Weapons 2 Collection"
                        ],
                    [
                        ["Revolver","Revolver","Switchblade","Desert Eagle","Desert Eagle","Desert Eagle","Desert Eagle","Desert Eagle","AP Pistol","AP Pistol","AP Pistol","Scorpion","Mini Uzi"],
                        "$267,000",
                        "The Handgun Collection"
                        ]
                    ],  # 3% 94-97
                [
                    [
                        ["Handcuffs","Handcuff Key","Heavy Pistol","Scorpion","Scorpion","Bullpump Rifle","AK-47","Assault Shotgun"],
                        "$332,000",
                        "The Handcuff Collection"
                        ],
                    [
                        ["Revolver","Switchblade","Switchblade","Battleaxe","Battleaxe","Tec9","Tec9","Mini AK-47","Combat MG"],
                        "$323,500",
                        "The Small Weapons Collection"
                        ],
                    [
                        ["Battleaxe","Battleaxe","Battleaxe","Switchblade","Switchblade","Special Carbine","Bullpump Rifle","AK-47"],
                        "$311,000",
                        "The Melee Collection"
                        ],
                    [
                        ["Heavy Pistol","Heavy Pistol","Tec9","Scorpion","Tommy Gun","Special Carbine","AK-47"],
                        "$301,000",
                        "The Rifle Collection"
                        ],
                    [
                        ["Desert Eagle","Desert Eagle","Tec9","Tec9","Scorpion","Scorpion","Mini Uzi","MP5","Special Carbine"],
                        "$321,000",
                        "The SMG Collection"
                        ],
                    [
                        ["Revolver","Desert Eagle","Desert Eagle","Scorpion","Scorpion","AP Pistol","Mini Uzi","Combat MG"],
                        "$315,500",
                        "The Small Weapons 2 Collection"
                        ],
                    [
                        ["Revolver","Revolver","Revolver","Desert Eagle","Desert Eagle","AP Pistol","AP Pistol","AP Pistol","Assault Shotgun","AK-47"],
                        "$300,500",
                        "The Handgun Collection"
                        ]
                    ],  # 2% 98-99
                [
                    [
                        ["Handcuffs","Handcuff Key","Heavy Pistol","Battleaxe","Scorpion","Scorpion","Mini Uzi","Tommy Gun","Carbine Rifle","AP Pistol","Assault Shotgun"],
                        "$376,500",
                        "The Handcuff Collection"
                        ],
                    [
                        ["Revolver","Switchblade","Tec9","Tec9","AP Pistol","Carbine Rifle","MG"],
                        "$371,500",
                        "The Small Weapons Collection"
                        ],
                    [
                        ["Battleaxe","Battleaxe","Battleaxe","Switchblade","Switchblade","Switchblade","Scorpion","Mini Uzi","Mini Uzi","Assault Shotgun","Mini AK-47","MP5"],
                        "$350,500",
                        "The Melee Collection"
                        ],
                    [
                        ["Sniper Rifle","Switchblade"],
                        "$420,000",
                        "The Rifle Collection"
                        ],
                    [
                        ["Sniper Rifle","Switchblade"],
                        "$420,000",
                        "The Sniper Collection"
                        ],
                    [
                        ["Sniper Rifle","Switchblade","Tommy Gun"],
                        "$475,000",
                        "The Rifle 2 Collection"
                        ],
                    [
                        ["Switchblade","Switchblade","Battleaxe","Desert Eagle","Desert Eagle","Tec9","AP Pistol","AP Pistol","AP Pistol","AP Pistol","Tommy Gun","Tommy Gun"],
                        "$349,500",
                        "The Handgun Collection"
                        ]
                    ]   # 1% 100
                ]
        }
        self.config.register_guild(**default_guild)

    @commands.has_any_role("Lead Admin","Community Manager", "Owner")
    @commands.guild_only()
    @commands.command()
    async def shipment(self, ctx, member: discord.Member):
        async with self.config.guild(ctx.guild).packages() as packages:
            percentage = random.randrange(0, 100)
            print(percentage)
            if (percentage <= 25):
                tier = "Tier 1"
                color = 0xb3f2ff
                package_number = random.randint(0, 6)
                final_package = packages[0][package_number]
                collection_items = final_package[0]
                collection_price = final_package[1]
                collection_name = final_package[2]
                await terms_of_service(ctx, color, tier, collection_items, collection_price, collection_name, member)
            elif (percentage >= 26) and (percentage <= 61):
                tier = "Tier 2"
                color = 0x146eff
                package_number = random.randint(0, 6)
                final_package = packages[1][package_number]
                collection_items = final_package[0]
                collection_price = final_package[1]
                collection_name = final_package[2]
                await terms_of_service(ctx, color, tier, collection_items, collection_price, collection_name, member)
            elif (percentage >= 62) and (percentage <= 77):
                tier = "Tier 3"
                color = 0x14ffad
                package_number = random.randint(0, 6)
                final_package = packages[2][package_number]
                collection_items = final_package[0]
                collection_price = final_package[1]
                collection_name = final_package[2]
                await terms_of_service(ctx, color, tier, collection_items, collection_price, collection_name, member)
            elif (percentage >= 78) and (percentage <= 88):
                tier = "Tier 4"
                color = 0xa53dff
                package_number = random.randint(0, 6)
                final_package = packages[3][package_number]
                collection_items = final_package[0]
                collection_price = final_package[1]
                collection_name = final_package[2]
                await terms_of_service(ctx, color, tier, collection_items, collection_price, collection_name, member)
            elif (percentage >= 89) and (percentage <= 93):
                tier = "Tier 5"
                color = 0xff52ff
                package_number = random.randint(0, 6)
                final_package = packages[4][package_number]
                collection_items = final_package[0]
                collection_price = final_package[1]
                collection_name = final_package[2]
                await terms_of_service(ctx, color, tier, collection_items, collection_price, collection_name, member)
            elif (percentage >= 94) and (percentage <= 97):
                tier = "Tier 6"
                color = 0xff9d3b
                package_number = random.randint(0, 6)
                final_package = packages[5][package_number]
                collection_items = final_package[0]
                collection_price = final_package[1]
                collection_name = final_package[2]
                await terms_of_service(ctx, color, tier, collection_items, collection_price, collection_name, member)
            elif (percentage >= 98) and (percentage <= 99):
                tier = "Tier 7"
                color = 0xff3b3b
                package_number = random.randint(0, 6)
                final_package = packages[6][package_number]
                collection_items = final_package[0]
                collection_price = final_package[1]
                collection_name = final_package[2]
                await terms_of_service(ctx, color, tier, collection_items, collection_price, collection_name, member)
            elif percentage == 100:
                tier = "Tier 8"
                color = 0xffeb3b
                package_number = random.randint(0, 6)
                final_package = packages[7][package_number]
                collection_items = final_package[0]
                collection_price = final_package[1]
                collection_name = final_package[2]
                await terms_of_service(ctx, color, tier, collection_items, collection_price, collection_name, member)
            else:
                pass
    
    @commands.has_any_role("Lead Admin","Community Manager", "Owner")
    @commands.guild_only()
    @commands.command(name="shipmentlist")
    async def shipment_list(self, ctx, member: discord.Member):


        collections = [
            ["Heavy Pistol","Switchblade","Handcuffs","Handcuff Key","AP Pistol","Scorpion","Mini Uzi","Assault Shotgun","Bullpump Shotgun","Tommy Gun","Mini AK-47","Combat MG","MG","Carbine Rifle","AK-47"],
            ["Heavy Pistol","Revolver","Desert Eagle","Switchblade","Battleaxe","Tec9","AP Pistol","Mini Uzi","MP5","Assault Shotgun","Special Carbine","Bullpump Rifle","Mini AK-47","Combat MG","MG","AK-47"],
            ["Heavy Pistol","Revolver","Battleaxe","Switchblade","Desert Eagle","Handcuffs","Handcuff Keys","Tec9","Scorpion","AP Pistol","Mini Uzi","MP5","Assault Shotgun","Bullpump Rifle","Special Carbine","Carbine Rifle","MG","AK-47"],
            ["Heavy Pistol","Revolver","Battleaxe","Desert Eagle","Tec9","Scorpion","Assault Shotgun","Tommy Gun","Special Carbine","Mini AK-47","AK-47","Sniper Rifle"],
            ["Heavy Pistol","Revolver","Battleaxe","Switchblade","Desert Eagle","Tec9","Scorpion","Mini Uzi","MP5","Tommy Gun","Special Carbine","AK-47"],
            ["Revolver","Switchblade","Handcuffs","Handcuff Keys","Battleaxe","Desert Eagle","Tec9","Scorpion","AP Pistol","Mini Uzi","Tommy Gun","MP5","Assault Shotgun","AK-47","Bullpump Rifle","Combat MG"],
            ["Heavy Pistol","Revolver","Switchblade","Battleaxe","Desert Eagle","Tec9","Scorpion","AP Pistol","Mini Uzi","Assault Shotgun","Tommy Gun","Special Carbine","AK-47"]
        ]
        collection_names = ["The Handcuff Collection","The Small Weapons Collection","The Melee Collection","The Rifle Collection","The SMG Collection","The Small Weapons 2 Collection","The Handgun Collection"]
        slist = discord.Embed(
            color = 0x2a9946,
            timestamp = datetime.datetime.now(),
            title = "NexusRP Gun Shipments"
        )

        counter = 0
        for collection in collections:
            slist.add_field(
                name = collection_names[counter],
                value = "\n".join(collection)
            )
            counter += 1

        slist.set_footer(
            text = "Copyright © 2020 NexusHub.io",
            icon_url = "https://cdn.discordapp.com/icons/699702073951912028/a_1d960abbbe922ff536e0d469dc4f518a.webp?size=128"
        )

        try:
            await member.send(embed = slist)
        except discord.errors.Forbidden:
            await ctx.send(f">>> {member.mention} has their DMs closed.")


        