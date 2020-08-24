from .querynrp_main import Querynrp

def setup(bot):
    bot.add_cog(Querynrp(bot))