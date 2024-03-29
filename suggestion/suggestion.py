import asyncio
import discord

from typing import Any, Optional
from discord.utils import get
from datetime import datetime, timedelta

from redbot.core import Config, checks, commands
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.antispam import AntiSpam

from redbot.core.bot import Red

Cog: Any = getattr(commands, "Cog", object)


class Suggestion(Cog):
    """
    Simple suggestion box, basically.

    **Use `[p]setsuggest setup` first.**
    Only admins can approve or reject suggestions.
    """

    __author__ = "saurichable"
    __version__ = "1.1.1"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=2115656421364, force_registration=True
        )
        self.antispam = {}
        self.config.register_guild(
            same=False, suggest_id=None, approve_id=None, reject_id=None, next_id=1
        )
        self.config.register_global(
            toggle=False, server_id=None, channel_id=None, next_id=1, ignore=[]
        )
        self.config.init_custom("SUGGESTION", 2)
        self.config.register_custom(
            "SUGGESTION",
            author=[],
            msg_id=0,
            finished=False,
            approved=False,
            rejected=False,
            reason=False,
            stext=None,
            rtext=None,
        )

    @commands.command()
    @commands.guild_only()
    @checks.bot_has_permissions(add_reactions=True)
    async def suggest(self, ctx: commands.Context, *, suggestion: str):
        """Suggest something. Message is required."""
        suggest_id = await self.config.guild(ctx.guild).suggest_id()
        if suggest_id is None:
            if await self.config.toggle() is True:
                if ctx.guild.id in await self.config.ignore():
                    return await ctx.send("Uh oh, suggestions aren't enabled.")
                global_guild = self.bot.get_guild(await self.config.server_id())
                channel = get(
                    global_guild.text_channels, id=await self.config.channel_id()
                )
            else:
                return await ctx.send("Uh oh, suggestions aren't enabled.")
        else:
            channel = get(ctx.guild.text_channels, id=suggest_id)
        if channel is None:
            return await ctx.send(
                "Uh oh, looks like your Admins haven't added the required channel."
            )

        if ctx.guild not in self.antispam:
            self.antispam[ctx.guild] = {}
        if ctx.author not in self.antispam[ctx.guild]:
            self.antispam[ctx.guild][ctx.author] = AntiSpam([(timedelta(days=1), 6)])
        if self.antispam[ctx.guild][ctx.author].spammy:
            return await ctx.send("Uh oh, you're doing this way too frequently.")

        embed = discord.Embed(color=await ctx.embed_colour(), description=suggestion)
        embed.set_author(
            name=f"Suggestion by {ctx.author.display_name}",
            icon_url=ctx.author.avatar_url,
        )
        embed.set_footer(
            text=f"Suggested by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})"
        )

        if suggest_id is None:
            if await self.config.toggle() is True:
                s_id = await self.config.next_id()
                await self.config.next_id.set(s_id + 1)
                server = 1
                content = f"Global suggestion #{s_id}"
        else:
            s_id = await self.config.guild(ctx.guild).next_id()
            await self.config.guild(ctx.guild).next_id.set(s_id + 1)
            server = ctx.guild.id
            content = f"**Suggestion #{s_id}**"

        msg = await channel.send(content=content, embed=embed)
        await msg.add_reaction("<:tick:445640284202729472>")
        await msg.add_reaction("<:wip:445659716329275413>")
        await msg.add_reaction("<:cross:445640325780865035>")

        async with self.config.custom("SUGGESTION", server, s_id).author() as author:
            author.append(ctx.author.id)
            author.append(ctx.author.name)
            author.append(ctx.author.discriminator)
        await self.config.custom("SUGGESTION", server, s_id).stext.set(suggestion)
        await self.config.custom("SUGGESTION", server, s_id).msg_id.set(msg.id)

        self.antispam[ctx.guild][ctx.author].stamp()
        await ctx.tick()
        try:
            await ctx.author.send(
                content="Your suggestion has been sent for approval!", embed=embed
            )
        except:
            return

    @checks.admin_or_permissions(manage_messages=True)
    @commands.command()
    @commands.guild_only()
    @checks.bot_has_permissions(manage_messages=True)
    async def approve(
        self,
        ctx: commands.Context,
        suggestion_id: int,
        is_global: Optional[bool] = False,
    ):
        """Approve a suggestion."""
        if is_global is True:
            if await self.config.toggle() is True:
                if ctx.author.id != self.bot.owner_id:
                    return await ctx.send("Uh oh, you're not my owner.")
                server = 1
                global_guild = self.bot.get_guild(await self.config.server_id())
                oldchannel = get(
                    global_guild.text_channels, id=await self.config.channel_id()
                )
            else:
                return await ctx.send("Global suggestions aren't enabled.")
        else:
            server = ctx.guild.id
            oldchannel = get(
                ctx.guild.text_channels,
                id=await self.config.guild(ctx.guild).suggest_id(),
            )
            channel = get(
                ctx.guild.text_channels,
                id=await self.config.guild(ctx.guild).approve_id(),
            )

        msg_id = await self.config.custom("SUGGESTION", server, suggestion_id).msg_id()
        if msg_id != 0:
            if (
                await self.config.custom("SUGGESTION", server, suggestion_id).finished()
                is True
            ):
                return await ctx.send("This suggestion has been finished already.")

        try:
            oldmsg = await oldchannel.fetch_message(id=msg_id)
        except:
            return await ctx.send("Uh oh, message with this ID doesn't exist.")
        embed = oldmsg.embeds[0]
        content = oldmsg.content

        op_info = await self.config.custom("SUGGESTION", server, suggestion_id).author()
        op_id = int(op_info[0])
        op = await self.bot.fetch_user(op_id)
        op_name = op.name
        op_avatar = op.avatar_url
        if op is None:
            op_name = str(op_info[1])
            op_avatar = ctx.guild.icon_url

        embed.set_author(
            name="Approved suggestion by {0}".format(op_name), icon_url=op_avatar
        )
        if is_global is True:
            await oldmsg.edit(content=content, embed=embed)
            try:
                await oldmsg.clear_reactions()
            except:
                pass
        else:
            if channel is not None:
                await oldmsg.delete()
                nmsg = await channel.send(content=content, embed=embed)
                await self.config.custom(
                    "SUGGESTION", server, suggestion_id
                ).msg_id.set(nmsg.id)
            else:
                if await self.config.guild(ctx.guild).same() is False:
                    await oldmsg.delete()
                    await self.config.custom(
                        "SUGGESTION", server, suggestion_id
                    ).msg_id.set(1)
                else:
                    await oldmsg.edit(content=content, embed=embed)
                    try:
                        await oldmsg.clear_reactions()
                    except:
                        pass
        await self.config.custom("SUGGESTION", server, suggestion_id).finished.set(True)
        await self.config.custom("SUGGESTION", server, suggestion_id).approved.set(True)
        await ctx.tick()

        try:
            await op.send(content="Your suggestion has been approved!", embed=embed)
        except:
            return

    @checks.admin_or_permissions(manage_messages=True)
    @commands.command()
    @commands.guild_only()
    @checks.bot_has_permissions(manage_messages=True)
    async def reject(
        self,
        ctx: commands.Context,
        suggestion_id: int,
        is_global: Optional[bool] = False,
        *,
        reason="",
    ):
        """Reject a suggestion. Reason is optional."""
        if is_global is True:
            if await self.config.toggle() is True:
                if ctx.author.id != self.bot.owner_id:
                    return await ctx.send("Uh oh, you're not my owner.")
                server = 1
                global_guild = self.bot.get_guild(await self.config.server_id())
                oldchannel = get(
                    global_guild.text_channels, id=await self.config.channel_id()
                )
            else:
                return await ctx.send("Global suggestions aren't enabled.")
        else:
            server = ctx.guild.id
            oldchannel = get(
                ctx.guild.text_channels,
                id=await self.config.guild(ctx.guild).suggest_id(),
            )
            channel = get(
                ctx.guild.text_channels,
                id=await self.config.guild(ctx.guild).reject_id(),
            )

        msg_id = await self.config.custom("SUGGESTION", server, suggestion_id).msg_id()
        if msg_id != 0:
            if (
                await self.config.custom("SUGGESTION", server, suggestion_id).finished()
                is True
            ):
                return await ctx.send("This suggestion has been finished already.")

        try:
            oldmsg = await oldchannel.fetch_message(id=msg_id)
        except:
            return await ctx.send("Uh oh, message with this ID doesn't exist.")
        embed = oldmsg.embeds[0]
        content = oldmsg.content

        op_info = await self.config.custom("SUGGESTION", server, suggestion_id).author()
        op_id = int(op_info[0])
        op = await self.bot.fetch_user(op_id)
        op_name = op.name
        op_avatar = op.avatar_url
        if op is None:
            op_name = str(op_info[1])
            op_avatar = ctx.guild.icon_url

        embed.set_author(
            name="Rejected suggestion by {0}".format(op_name), icon_url=op_avatar
        )

        if reason:
            embed.add_field(name="Reason:", value=reason, inline=False)
            await self.config.custom("SUGGESTION", server, suggestion_id).reason.set(
                True
            )
            await self.config.custom("SUGGESTION", server, suggestion_id).rtext.set(
                reason
            )

        if is_global is True:
            await oldmsg.edit(content=content, embed=embed)
            try:
                await oldmsg.clear_reactions()
            except:
                pass
        else:
            if channel is not None:
                await oldmsg.delete()
                nmsg = await channel.send(content=content, embed=embed)
                await self.config.custom(
                    "SUGGESTION", server, suggestion_id
                ).msg_id.set(nmsg.id)
            else:
                if await self.config.guild(ctx.guild).same() is False:
                    await oldmsg.delete()
                    await self.config.custom(
                        "SUGGESTION", server, suggestion_id
                    ).msg_id.set(1)
                else:
                    await oldmsg.edit(content=content, embed=embed)
                    try:
                        await oldmsg.clear_reactions()
                    except:
                        pass
        await self.config.custom("SUGGESTION", server, suggestion_id).finished.set(True)
        await self.config.custom("SUGGESTION", server, suggestion_id).rejected.set(True)
        await ctx.tick()

        try:
            await op.send(content="Your suggestion has been rejected!", embed=embed)
        except:
            return

    @checks.admin_or_permissions(manage_messages=True)
    @commands.command()
    @commands.guild_only()
    @checks.bot_has_permissions(manage_messages=True)
    async def addreason(
        self,
        ctx: commands.Context,
        suggestion_id: int,
        is_global: Optional[bool] = False,
        *,
        reason: str,
    ):
        """Add a reason to a rejected suggestion.
        
        Only works for non global suggestions."""
        if is_global is True:
            if await self.config.toggle() is True:
                if ctx.author.id != self.bot.owner_id:
                    return await ctx.send("Uh oh, you're not my owner.")
                server = 1
                global_guild = self.bot.get_guild(await self.config.server_id())
                channel = get(
                    global_guild.text_channels, id=await self.config.channel_id()
                )
            else:
                return await ctx.send("Global suggestions aren't enabled.")
        else:
            server = ctx.guild.id
            if await self.config.guild(ctx.guild).same() is False:
                channel = get(
                    ctx.guild.text_channels,
                    id=await self.config.guild(ctx.guild).reject_id(),
                )
            else:
                channel = get(
                    ctx.guild.text_channels,
                    id=await self.config.guild(ctx.guild).suggest_id(),
                )

        msg_id = await self.config.custom("SUGGESTION", server, suggestion_id).msg_id()
        if msg_id != 0:
            if (
                await self.config.custom("SUGGESTION", server, suggestion_id).rejected()
                is False
            ):
                return await ctx.send("This suggestion hasn't been rejected.")
            if (
                await self.config.custom("SUGGESTION", server, suggestion_id).reason()
                is True
            ):
                return await ctx.send("This suggestion already has a reason.")

            try:
                content, embed = await self._build_suggestion(
                    ctx, ctx.author.id, ctx.guild.id, suggestion_id, is_global
                )
            except:
                return
            embed.add_field(name="Reason:", value=reason, inline=False)
            try:
                msg = await channel.fetch_message(id=msg_id)
                await msg.edit(content=content, embed=embed)
            except:
                pass
        await self.config.custom("SUGGESTION", server, suggestion_id).reason.set(True)
        await self.config.custom("SUGGESTION", server, suggestion_id).rtext.set(reason)
        await ctx.tick()

    @checks.admin_or_permissions(manage_messages=True)
    @commands.command()
    @commands.guild_only()
    async def showsuggestion(
        self,
        ctx: commands.Context,
        suggestion_id: int,
        is_global: Optional[bool] = False,
    ):
        """Show a suggestion."""
        try:
            content, embed = await self._build_suggestion(
                ctx, ctx.author.id, ctx.guild.id, suggestion_id, is_global
            )
        except:
            return
        await ctx.send(content=content, embed=embed)

    @checks.admin_or_permissions(manage_messages=True)
    @commands.group(autohelp=True)
    @commands.guild_only()
    async def setsuggest(self, ctx: commands.Context):
        """Suggestion settings"""
        pass

    @checks.bot_has_permissions(manage_channels=True)
    @setsuggest.command(name="setup")
    async def setsuggest_setup(self, ctx: commands.Context):
        """ Go through the initial setup process. """
        bot = self.bot
        await self.config.guild(ctx.guild).same.set(False)
        await self.config.guild(ctx.guild).suggest_id.set(None)
        await self.config.guild(ctx.guild).approve_id.set(None)
        await self.config.guild(ctx.guild).reject_id.set(None)
        predchan = MessagePredicate.valid_text_channel(ctx)
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(send_messages=True),
        }
        msg = await ctx.send("Do you already have your channel(s) done?")
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        try:
            await bot.wait_for("reaction_add", timeout=30, check=pred)
        except asyncio.TimeoutError:
            await msg.delete()
            return await ctx.send("You took too long. Try again, please.")
        if pred.result is False:
            await msg.delete()
            suggestions = get(ctx.guild.text_channels, name="suggestions")
            if suggestions is None:
                suggestions = await ctx.guild.create_text_channel(
                    "suggestions", overwrites=overwrites, reason="Suggestion cog setup"
                )
            await self.config.guild(ctx.guild).suggest_id.set(suggestions.id)

            msg = await ctx.send(
                "Do you want to use the same channel for approved and rejected suggestions? (If yes, they won't be reposted anywhere, only their title will change accordingly.)"
            )
            start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
            pred = ReactionPredicate.yes_or_no(msg, ctx.author)
            try:
                await bot.wait_for("reaction_add", timeout=30, check=pred)
            except asyncio.TimeoutError:
                await msg.delete()
                return await ctx.send("You took too long. Try again, please.")
            if pred.result is True:
                await msg.delete()
                await self.config.guild(ctx.guild).same.set(True)
            else:
                await msg.delete()
                approved = get(ctx.guild.text_channels, name="approved-suggestions")
                if approved is None:
                    msg = await ctx.send(
                        "Do you want to have an approved suggestions channel?"
                    )
                    start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
                    pred = ReactionPredicate.yes_or_no(msg, ctx.author)
                    try:
                        await bot.wait_for("reaction_add", timeout=30, check=pred)
                    except asyncio.TimeoutError:
                        await msg.delete()
                        return await ctx.send("You took too long. Try again, please.")
                    if pred.result is True:
                        approved = await ctx.guild.create_text_channel(
                            "approved-suggestions",
                            overwrites=overwrites,
                            reason="Suggestion cog setup",
                        )
                        await self.config.guild(ctx.guild).approve_id.set(approved.id)
                    await msg.delete()
                else:
                    await self.config.guild(ctx.guild).approve_id.set(approved.id)

                rejected = get(ctx.guild.text_channels, name="rejected-suggestions")
                if rejected is None:
                    msg = await ctx.send(
                        "Do you want to have a rejected suggestions channel?"
                    )
                    start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
                    pred = ReactionPredicate.yes_or_no(msg, ctx.author)
                    try:
                        await bot.wait_for("reaction_add", timeout=30, check=pred)
                    except asyncio.TimeoutError:
                        await msg.delete()
                        return await ctx.send("You took too long. Try again, please.")
                    if pred.result is True:
                        rejected = await ctx.guild.create_text_channel(
                            "rejected-suggestions",
                            overwrites=overwrites,
                            reason="Suggestion cog setup",
                        )
                        await self.config.guild(ctx.guild).reject_id.set(rejected.id)
                    await msg.delete()
                else:
                    await self.config.guild(ctx.guild).reject_id.set(rejected.id)

        else:
            await msg.delete()
            msg = await ctx.send(
                "Mention the channel where you want me to post new suggestions."
            )
            try:
                await bot.wait_for("message", timeout=30, check=predchan)
            except asyncio.TimeoutError:
                await msg.delete()
                return await ctx.send("You took too long. Try again, please.")
            suggestion = predchan.result
            await self.config.guild(ctx.guild).suggest_id.set(suggestion.id)
            await msg.delete()

            msg = await ctx.send(
                "Do you want to use the same channel for approved and rejected suggestions? (If yes, they won't be reposted anywhere, only their title will change accordingly.)"
            )
            start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
            pred = ReactionPredicate.yes_or_no(msg, ctx.author)
            try:
                await bot.wait_for("reaction_add", timeout=30, check=pred)
            except asyncio.TimeoutError:
                await msg.delete()
                return await ctx.send("You took too long. Try again, please.")
            if pred.result is True:
                await msg.delete()
                await self.config.guild(ctx.guild).same.set(True)
            else:
                await msg.delete()
                msg = await ctx.send(
                    "Do you want to have an approved suggestions channel?"
                )
                start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
                pred = ReactionPredicate.yes_or_no(msg, ctx.author)
                try:
                    await bot.wait_for("reaction_add", timeout=30, check=pred)
                except asyncio.TimeoutError:
                    await msg.delete()
                    return await ctx.send("You took too long. Try again, please.")
                if pred.result is True:
                    await msg.delete()
                    msg = await ctx.send(
                        "Mention the channel where you want me to post approved suggestions."
                    )
                    try:
                        await bot.wait_for("message", timeout=30, check=predchan)
                    except asyncio.TimeoutError:
                        await msg.delete()
                        return await ctx.send("You took too long. Try again, please.")
                    approved = predchan.result
                    await self.config.guild(ctx.guild).approve_id.set(approved.id)
                await msg.delete()

                msg = await ctx.send(
                    "Do you want to have a rejected suggestions channel?"
                )
                start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
                pred = ReactionPredicate.yes_or_no(msg, ctx.author)
                try:
                    await bot.wait_for("reaction_add", timeout=30, check=pred)
                except asyncio.TimeoutError:
                    await msg.delete()
                    return await ctx.send("You took too long. Try again, please.")
                if pred.result is True:
                    await msg.delete()
                    msg = await ctx.send(
                        "Mention the channel where you want me to post rejected suggestions."
                    )
                    try:
                        await bot.wait_for("message", timeout=30, check=predchan)
                    except asyncio.TimeoutError:
                        await msg.delete()
                        return await ctx.send("You took too long. Try again, please.")
                    rejected = predchan.result
                    await self.config.guild(ctx.guild).reject_id.set(rejected.id)
                await msg.delete()

        await ctx.send(
            "You have finished the setup! Please, move your channels to the category you want them in."
        )

    @setsuggest.group(autohelp=True)
    @checks.is_owner()
    @commands.guild_only()
    async def setglobal(self, ctx: commands.Context):
        """Global suggestions settings.

        There is nothing like approved or rejected channels because global suggestions are meant to be for the bot only and will only work if it is sent in a server where normal suggestions are disabled."""
        pass

    @setglobal.command(name="toggle")
    async def setsuggest_setglobal_toggle(
        self, ctx: commands.Context, on_off: bool = None
    ):
        """Toggle global suggestions. 
        If `on_off` is not provided, the state will be flipped."""
        target_state = (
            on_off if on_off is not None else not (await self.config.toggle())
        )
        await self.config.toggle.set(target_state)
        if target_state:
            await ctx.send("Global suggestions are now enabled.")
        else:
            await ctx.send("Global suggestions are now disabled.")

    @setglobal.command(name="channel")
    async def setsuggest_setglobal_channel(
        self,
        ctx: commands.Context,
        server: discord.Guild = None,
        channel: discord.TextChannel = None,
    ):
        """Add channel where global suggestions should be sent."""
        if not server:
            server = ctx.guild
        if not channel:
            channel = ctx.channel
        await self.config.server_id.set(server.id)
        await self.config.channel_id.set(channel.id)
        await ctx.send(f"{channel.mention} has been saved for global suggestions.")

    @setglobal.command(name="ignore")
    async def setsuggest_setglobal_ignore(
        self, ctx: commands.Context, server: discord.Guild = None
    ):
        """ Ignore suggestions from the server. """
        if not server:
            server = ctx.guild
        if server.id not in await self.config.ignore():
            async with self.config.ignore() as ignore:
                ignore.append(server.id)
            await ctx.send(
                "{0} has been added into the ignored list.".format(server.name)
            )
        else:
            await ctx.send("{0} is already in the ignored list.".format(server.name))

    @setglobal.command(name="unignore")
    async def setsuggest_setglobal_unignore(
        self, ctx: commands.Context, server: discord.Guild = None
    ):
        """ Remove server from the ignored list. """
        if not server:
            server = ctx.guild
        if server.id in await self.config.ignore():
            async with self.config.ignore() as ignore:
                ignore.remove(server.id)
            await ctx.send(
                "{0} has been removed from the ignored list.".format(server.name)
            )
        else:
            await ctx.send("{0} already isn't in the ignored list.".format(server.name))

    async def _build_suggestion(
        self, ctx, author_id, server_id, suggestion_id, is_global
    ):
        if is_global is True:
            if await self.config.toggle() is True:
                if author_id != self.bot.owner_id:
                    return await ctx.send("Uh oh, you're not my owner.")
                server = 1
                if (
                    await self.config.custom(
                        "SUGGESTION", server, suggestion_id
                    ).msg_id()
                    != 0
                ):
                    content = f"Global suggestion #{suggestion_id}"
                else:
                    return await ctx.send(
                        "Uh oh, that suggestion doesn't seem to exist."
                    )
            else:
                return await ctx.send("Global suggestions aren't enabled.")
        if is_global is False:
            server = server_id
            if (
                await self.config.custom("SUGGESTION", server, suggestion_id).msg_id()
                != 0
            ):
                content = f"Suggestion #{suggestion_id}"
            else:
                return await ctx.send("Uh oh, that suggestion doesn't seem to exist.")

        op_info = await self.config.custom("SUGGESTION", server, suggestion_id).author()
        op_id = int(op_info[0])
        op = await self.bot.fetch_user(op_id)
        if op is not None:
            op_name = op.name
            op_discriminator = op.discriminator
            op_avatar = op.avatar_url
        else:
            op_name = str(op_info[1])
            op_discriminator = int(op_info[2])
            op_avatar = ctx.guild.icon_url

        if (
            await self.config.custom("SUGGESTION", server, suggestion_id).finished()
            is False
        ):
            atext = f"Suggestion by {op_name}"
        else:
            if (
                await self.config.custom("SUGGESTION", server, suggestion_id).approved()
                is True
            ):
                atext = f"Approved suggestion by {op_name}"
            else:
                if (
                    await self.config.custom(
                        "SUGGESTION", server, suggestion_id
                    ).rejected()
                    is True
                ):
                    atext = f"Rejected suggestion by {op_name}"

        embed = discord.Embed(
            color=await ctx.embed_colour(),
            description=await self.config.custom(
                "SUGGESTION", server, suggestion_id
            ).stext(),
        )
        embed.set_author(name=atext, icon_url=op_avatar)
        embed.set_footer(text=f"Suggested by {op_name}#{op_discriminator} ({op_id})")

        if (
            await self.config.custom("SUGGESTION", server, suggestion_id).reason()
            is True
        ):
            embed.add_field(
                name="Reason:",
                value=await self.config.custom(
                    "SUGGESTION", server, suggestion_id
                ).rtext(),
                inline=False,
            )

        return content, embed
