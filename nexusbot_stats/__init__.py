from .stats_main import StatsMain

def setup(bot):
    bot.add_cog(StatsMain(bot))