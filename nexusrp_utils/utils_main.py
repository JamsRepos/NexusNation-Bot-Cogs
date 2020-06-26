import discord, datetime, asyncio, aiohttp
from redbot.core import commands, checks, Config

def guild_check():
    def is_nexusrp(ctx):
        if ctx.guild.id == 699702073951912028:
            return True
    return commands.check(is_nexusrp)

async def car_sale_embed(ctx, seller, question):
    embed = discord.Embed(
        title=question,
        color=0x2a9946
    )
    await seller.send(embed=embed)

class nexusUtils(commands.Cog):

    __author__ = "Raff"
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    # Nexus RP instagram reaction adder
    @commands.Cog.listener()
    async def on_message(self, message):
        ...
        discord_server = discord.utils.get(self.bot.guilds, id=699702073951912028)
        bot_commands_channel = discord.utils.get(discord_server.text_channels, id=713173661523116043)
        ...
        if (message.channel.id == 713173512533311528):
            if (":ig:" not in message.content):
                await message.delete()
                try:
                    message.author.send("Please format your instagram posts properly by including the `:ig:` emoji")
                except discord.errors.Forbidden:
                    bot_commands_channel.send(f"{message.author.mention} Please format your instagram posts properly by including the :ig: emoji")
            if (len(message.attachments)>0):
                message.add_reaction("❤️")
        else: 
            pass


    # sell cars
    @guild_check()
    @commands.group(name="sell")
    async def sell_command(self, ctx):
        if ctx.invoked_subcommand is None:
            pass
    
    @sell_command.command(name="vehicle")
    async def sell_car(self, ctx):
        ...
        car_sales_channel = discord.utils.get(ctx.guild.channels, id=723090935747051531)
        ...
        seller = ctx.author
        ...
        def check(message): 
            return (ctx.author == message.author) and (isinstance(message.channel, discord.DMChannel))
        ...
        q1 = "Please enter the make/model of this vehicle"
        q2 = "Please enter the price you are selling this vehicle for"
        q3 = "Please enter a description of this vehicle"
        q4 = "Please enter your phone number"
        q5 = "Please send an image of the vehicle you are selling"
        ...
        try:
            await car_sale_embed(ctx, seller, q1)
            a1 = await self.bot.wait_for("message", check=check, timeout=3)
            await car_sale_embed(ctx, seller, q2)
            a2 = await self.bot.wait_for("message", check=check, timeout=300)
            await car_sale_embed(ctx, seller, q3)
            a3 = await self.bot.wait_for("message", check=check, timeout=300)
            await car_sale_embed(ctx, seller, q4)
            a4 = await self.bot.wait_for("message", check=check, timeout=300)
            ...
            valid_image = False
            while not valid_image:
                await car_sale_embed(ctx, seller, q5)
                product_image = await self.bot.wait_for("message", check=check, timeout=300)
                if len(product_image.attachments)>0:
                    if (product_image.attachments[0].url)[-3:] in ("png", "jpg","gif"):
                        image_url = product_image.attachments[0].url
                        valid_image = True
                        break
                    else:
                        await seller.send("`Filetype not supported please try again`")
                        continue
                else:
                    await seller.send("`Please upload an image`")
                    continue
        except asyncio.TimeoutError:
            await ctx.channel.send(f"{ctx.author.mention} you ran out of time to enter all necessasry information for your car sale.")
        except discord.errors.Forbidden:
            await ctx.channel.send(f"{ctx.author.mention} your DMs are closed. Please alter your privacy settings to put a vehicle up for sale.")
        else:
            sale_embed = discord.Embed(
                colour=0x2a9946,
                timestamp = datetime.datetime.utcnow()
            )
            sale_embed.set_author(
                name=f"{seller.display_name} is selling a vehicle",
                icon_url=seller.avatar_url
            )
            sale_embed.add_field(
                name="Make/Model",
                value=a1.content,
                inline=False
            )
            sale_embed.add_field(
                name="Price",
                value=a2.content,
                inline=False
            )
            sale_embed.add_field(
                name="Description",
                value=a3.content,
                inline=False
            )
            sale_embed.add_field(
                name="Contact",
                value=a4.content,
                inline=False
            )
            sale_embed.set_image(
                url = image_url
            )
            sale_embed.set_footer(
                text = "Copyright © 2020 NexusHub.io",
                icon_url = "https://cdn.discordapp.com/icons/699702073951912028/a_1d960abbbe922ff536e0d469dc4f518a.webp?size=128"
            )
            ...
            await car_sales_channel.send(embed=sale_embed)
