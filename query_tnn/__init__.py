from .tnn_main import QueryTNN

def setup(bot):
    bot.add_cog(QueryTNN(bot))