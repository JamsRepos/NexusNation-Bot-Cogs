from .helpmenu import HelpMenu


def setup(bot):
    bot.add_cog(HelpMenu(bot))
