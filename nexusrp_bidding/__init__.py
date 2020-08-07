from .bidding import Bidding

def setup(bot):
    bot.add_cog(Bidding(bot))