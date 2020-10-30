from .discordmembers import DiscordMembers


def setup(bot):
    bot.add_cog(DiscordMembers(bot))
