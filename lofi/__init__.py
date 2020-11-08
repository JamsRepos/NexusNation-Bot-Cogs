from .lofi import Lofi


def setup(bot):
    bot.add_cog(Lofi(bot))
