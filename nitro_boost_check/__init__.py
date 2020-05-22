from .nitro_channels_main import NitroCustomChannels

def setup(bot):
    bot.add_cog(NitroCustomChannels(bot))
