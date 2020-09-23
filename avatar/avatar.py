import discord
from redbot.core import commands
from redbot.core import checks


BaseCog = getattr(commands, "Cog", object)

class Avatar(BaseCog):
	"""View a user's avatar"""

	def __init__(self,bot):
		self.bot = bot
    
	@commands.command(pass_context=True)
	async def avatar(self, ctx, user: discord.Member=None):
		"""Embed profile image!"""
		author = ctx.message.author
		em = discord.Embed(colour=(await ctx.embed_colour()))
		if not user:
			user = author
		if user.avatar_url:
			em.set_image(url=user.avatar_url)
		else:
			em.set_image(url=user.default_avatar_url)
		await ctx.send(embed=em)
