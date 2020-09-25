from .main import BotInfo


async def setup(bot):
    cog = BotInfo(bot)
    bot.add_cog(cog)
