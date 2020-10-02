from .claim_twitch import Claim_Twitch

def setup(bot):
    bot.add_cog(Claim_Twitch(bot))