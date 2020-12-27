from redbot.core.utils.menus import menu, next_page, prev_page, close_menu

async def skip_current(
    ctx, pages, controls, message, page, timeout, emoji
    ):
    if message:
        skip_com = ctx.bot.get_command("skip")
        output = await ctx.invoke(skip_com)
        await message.delete()
        return output
        

async def pause_current(
    ctx, pages, controls, message, page, timeout, emoji
    ):
    if message:
        pause_com = ctx.bot.get_command("pause")
        output = await ctx.invoke(pause_com)
        await message.delete()
        return output

async def stop_current(
    ctx, pages, controls, message, page, timeout, emoji
    ):
    if message:
        stop_com = ctx.bot.get_command("stop")
        output = await ctx.invoke(stop_com)
        await message.delete()
        return output

async def prev_current(
    ctx, pages, controls, message, page, timeout, emoji
):
    if message:
        prev_com = ctx.bot.get_command("prev")
        output = await ctx.invoke(prev_com)
        await message.delete()
        return output

async def shuffle(
    ctx, pages, controls, message, page, timeout, emoji
):
    if message:
        prev_com = ctx.bot.get_command("shuffle")
        output = await ctx.invoke(prev_com)
        await message.delete()
        return output

async def repeat(
    ctx, pages, controls, message, page, timeout, emoji
):
    if message:
        prev_com = ctx.bot.get_command("repeat")
        output = await ctx.invoke(prev_com)
        await message.delete()
        return output

async def queue(
    ctx, pages, controls, message, page, timeout, emoji
):
    if message:
        prev_com = ctx.bot.get_command("queue")
        output = await ctx.invoke(prev_com)
        await message.delete()
        return output

async def lyrics(
    ctx, pages, controls, message, page, timeout, emoji
):
    if message:
        prev_com = ctx.bot.get_command("lyrics playing")
        output = await ctx.invoke(prev_com)
        await message.delete()
        return output

controls = {
    "⏮️": prev_current,
    "⏹️": stop_current,
    "⏯️": pause_current,
    "⏭️": skip_current,
    "🔀": shuffle,
    "🔃": repeat,
    "📋": queue,
    "🎙️": lyrics,
    "\N{CROSS MARK}": close_menu
    }
