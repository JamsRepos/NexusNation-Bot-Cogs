import datetime
import lavalink
from redbot.core import commands

async def player_check(ctx):
    if not (cog := ctx.bot.get_cog("Audio").player_check()):
        return False

async def get_song_config(ctx):
    if not (cog := ctx.bot.get_cog("Audio")):
        return False
    guild_data = await cog.config.guild(ctx.guild).all()
    global_data = await cog.config.all()

    shuffle = guild_data["shuffle"]
    repeat = guild_data["repeat"]
    autoplay = guild_data["auto_play"]

    text = ""
    text += (
        "Auto-Play"
        + ": "
        + ("\N{WHITE HEAVY CHECK MARK}" if autoplay else "\N{CROSS MARK}")
    )
    text += (
        (" | " if text else "")
        + "Shuffle"
        + ": "
        + ("\N{WHITE HEAVY CHECK MARK}" if shuffle else "\N{CROSS MARK}")
    )
    text += (
        (" | " if text else "")
        + "Repeat"
        + ": "
        + ("\N{WHITE HEAVY CHECK MARK}" if repeat else "\N{CROSS MARK}")
    )
    return text

async def format_time(time: int) -> str:
    """ Formats the given time into DD:HH:MM:SS """
    seconds = time / 1000
    days, seconds = divmod(seconds, 24 * 60 * 60)
    hours, seconds = divmod(seconds, 60 * 60)
    minutes, seconds = divmod(seconds, 60)
    day = ""
    hour = ""
    if days:
        day = "%02d:" % days
    if hours or day:
        hour = "%02d:" % hours
    minutes = "%02d:" % minutes
    sec = "%02d" % seconds
    return f"{day}{hour}{minutes}{sec}"

async def draw_time(ctx) -> str:
    player = lavalink.get_player(ctx.guild.id)
    paused = player.paused
    pos = player.position or 1
    dur = getattr(player.current, "length", player.position or 1)
    sections = 23
    loc_time = round((pos / dur if dur != 0 else pos) * sections)
    bar = "\N{BOX DRAWINGS HEAVY HORIZONTAL}"
    # seek = "<:offlineicon:482526153840656385>"
    seek = "<a:pingu_track:783129078546300938>"
    end_track = "⏭️"
    if paused:
        msg = "\N{DOUBLE VERTICAL BAR}\N{VARIATION SELECTOR-16}"
    else:
        msg = "\N{BLACK RIGHT-POINTING TRIANGLE}\N{VARIATION SELECTOR-16}"
    for i in range(sections):
        if i == loc_time:
            msg += seek
        else:
            msg += bar
    return msg + end_track

async def control_list(ctx) -> str:
    controllist = """
    ⏮️`Previous      :` Skip to the previously played song
    ⏹`Stop          :` Stop playback and clear the queue
    ⏯️`Pause/Play    :` Pause or resume a playing track
    ⏭️`Skip          :` Skip to the next song
    🔀`Shuffle       :` Toggle shuffle of songs
    🔃`Repeat        :` Toggle repeat on current song
    📋`Song queue    :` List the songs in the queue
    🎙️`Lyrics        :` Show lyrics for the current song
    """
    return controllist