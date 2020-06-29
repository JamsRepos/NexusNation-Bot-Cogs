from .shipments import Shipments

def setup(bot):
    bot.add_cog(Shipments(bot))