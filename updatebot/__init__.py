from .updatebot import UpdateBot


def setup(bot):
    bot.add_cog(UpdateBot(bot))
