import discord
from redbot.core import commands
from redbot.core import checks


class Snapchat(commands.Cog):
    """Share your snapcodes!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=False, aliases=["snapcode"])
    async def snapchat(self, ctx, *, username):
        """View snapcodes!"""

        if username:
            username = username.strip()
            em = discord.Embed(colour=0xfffc00, timestamp=__import__("datetime").datetime.utcnow())
            em.set_author(name="{}'s Snapcode:".format(username))
            em.set_image(
                url="https://feelinsonice-hrd.appspot.com/web/deeplink/snapcode?username={}&type=PNG".format(
                    username
                )
            )
            await ctx.send(embed=em)
        else:
            await ctx.send("Please specify a snapchat username")
