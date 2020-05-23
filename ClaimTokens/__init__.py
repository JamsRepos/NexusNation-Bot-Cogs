from .claim import Claim

def setup(bot):
    bot.add_cog(Claim(bot))