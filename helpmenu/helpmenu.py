import datetime
import os
import discord
from redbot.core import checks, commands
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
import lavalink
from redbot.core.utils.chat_formatting import pagify


try:
    import psutil

    psutilAvailable = True
except ImportError:
    psutilAvailable = False


class HelpMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.command(hidden=True)
    async def help(self, ctx, *, command=None):
        prefix_string = ctx.prefix
        dpy_version = discord.__version__
        brambleid = "<@167990165258633216>"
        """Help is on the way"""
        desc = """Hello, I am `Nexus`!
        I am a administration, utility, music and fun bot packed with unique commands and fun features to offer!
        I was written in Python using [`Discord.py`](https://github.com/Rapptz/discord.py) ({}) on the [`Red`](https://github.com/Cog-Creators/Red-DiscordBot) framework.
        If you want to invite me to your guild, click [`here`](https://discordapp.com/oauth2/authorize?client_id=409819492655562767&scope=bot&permissions=8) or use `{}invite`!
        
        Here you will find pages of my different sections and the commands in them.""".format(dpy_version, prefix_string)

        since = ctx.bot.uptime.strftime("%d-%m-%y at %H:%M:%S")
        title = "Nexus Help Menu:"
        author = ctx.author
        await ctx.tick()
        message = "test"
        guild_nexusnation = 269912749327253504
        Test = None

        connections = len(lavalink.all_players())
        if connections == 0:
            connections = "No connections."
        else:
            connections = len(lavalink.all_players())

        # PAGE 1
        page1 = discord.Embed(description=desc, colour=(await ctx.embed_colour()))
        page1.set_author(name=title, icon_url=ctx.bot.user.avatar_url)
        page1.add_field(name="Server Prefix", value="`{}`".format(prefix_string))
        page1.set_thumbnail(url=ctx.bot.user.avatar_url)
        page1.add_field(name="Streams", value=connections)
        page1.set_footer(text="Page 1/3 | Last Restart: {}".format(since))

        # PAGE 2
        generalcommands = ["ping", "avatar", "snapchat", "invite", "contact", "prefix", "stats," "userinfo", "serverinfo"]
        moderationcommands = ["prune", "cleanup", "ban", "hackban", "ignore", "kick", "modset", "mute", "names", "rename", "slowmode", "softban", "tempban", "unban", "unignore", "unmute", "modlogsetup", "modlogset", "case", "casefor", "reason"]
        musiccommands = ["audioset", "audiostats", "bump", "disconnect", "summon", "local", "np", "pause", "percent", "play", "playlist", "prev", "queue", "remove", "repeat", "search", "seek", "shuffle", "skip", "stop", "volume", "lyrics"]
        nexusonlycommands = ["claimtokens", "tokenreminder", "claimvip", "vipreminder", "suggest", "missing", "appeal", "apply", "report", "calladmin", "differs", "bugreport", "vip", "role", "profile", "profileset", "background", "toplevel"]
        nexuscommands = ["jb", "ttt", "surf", "bhop"]
        utilitycommands = ["starboard", "customcom", "filter", "filterset", "autorole", "alias", "google", "gif", "imgtfy", "imgur", "covid", "color", "autoroom", "autoroomset"]

        # generalcommands = """`ping" `avatar` `snapchat` `invite` `contact` `prefix` `stats` `userinfo` `serverinfo`"""
        # moderationcommands = """`prune` `cleanup` `ban` `hackban` `ignore` `kick` `modset` `mute` `names` `rename` `slowmode` `softban` `tempban` `unban` `unignore` `unmute` `modlogsetup` `modlogset` `case` `casefor` `reason`"""
        # musiccommands = """`audioset` `audiostats` `bump` `disconnect` `summon` `local` `np` `pause` `percent` `play` `playlist` `prev` `queue` `remove` `repeat` `search` `seek` `shuffle` `skip` `stop` `volume` `lyrics`"""
        # nexusonlycommands = """`claimtokens` `tokenreminder` `claimvip` `vipreminder` `suggest` `missing` `appeal` `apply` `report` `calladmin` `differs` `bugreport` `vip` `role `profile` `profileset` `background` `toplevel`"""
        # nexuscommands = """`jb` `ttt` `surf` `bhop`"""
        # utilitycommands = """`starboard` `customcom`  `filter` `filterset` `autorole` `alias` `google` `gif` `imgtfy` `imgur` `covid` `color` `autoroom` `autoroomset`"""
        page2 = discord.Embed(colour=(await ctx.embed_colour()))
        page2.set_author(name=title, icon_url=ctx.bot.user.avatar_url)
        page2.add_field(
            name="Server Prefix", value="`{}`".format((prefix_string)), inline=False
        )
        page2.add_field(name="General Commands - 9", value="`" + (''.join(map(str, arena)) + "`", inline=False)
        page2.add_field(name="Moderation Commands - 21", value=moderationcommands, inline=False)
        page2.add_field(name="Music Commands - 25", value=musiccommands, inline=False)
        if ctx.message.guild.id == guild_nexusnation:
            page2.add_field(name="NexusNation Guild Only Commands - 18", value=nexusonlycommands, inline=False)
        page2.add_field(name="Nexus Stats Commands - 4", value=nexuscommands, inline=False)
        page2.add_field(name="Utility Commands - 15", value=utilitycommands, inline=False)
        page2.set_footer(text="Page 2/3 | Last Restart: {}".format(since))

        # PAGE 3
        info = "Looking for more information like statistics? Run `{}stats`.".format((prefix_string))
        page3 = discord.Embed(description=info, colour=(await ctx.embed_colour()))
        page3.set_author(name=title, icon_url=ctx.bot.user.avatar_url)
        botowner = "Nexus Hub"
        page3.add_field(name="Developers", value=botowner)
        page3.add_field(
            name="Libs",
            value="[`Discord.py`](https://github.com/Rapptz/discord.py)\n[`Red`](https://github.com/Cog-Creators/Red-DiscordBot)\n[`Lavalink.py`](https://github.com/Devoxin/Lavalink.py)",
        )
        page3.set_footer(text=f"Page 3/3 | Last Restart: {since}")

        embeds = [page1, page2, page3]
        if command == "all":
            await ctx.bot.send_help_for(ctx, Test)
        if command is None:
            await menu(ctx, embeds, DEFAULT_CONTROLS)
        if command is not None:
            await ctx.bot.send_help_for(ctx, command)
        return
