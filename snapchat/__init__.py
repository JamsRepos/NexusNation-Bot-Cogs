from .snapchat import Snapchat

def setup(bot):
    bot.add_cog(Snapchat(bot))
