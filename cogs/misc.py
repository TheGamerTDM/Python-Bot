import time

import discord
from discord.ext import commands

import utils

import random
import re
import calendar
import datetime
import psutil


def _command_signature(cmd):
    result = [cmd.qualified_name]
    if cmd.usage:
        result.append(cmd.usage)
        return " ".join(result)

    params = cmd.clean_params
    if not params:
        return " ".join(result)

    for name, param in params.items():
        if param.default is not param.empty:
            # We don't want None or '' to trigger the [name=value] case and instead it should
            # do [name] since [name=None] or [name=] are not exactly useful for the user.
            should_print = (
                param.default
                if isinstance(param.default, str)
                else param.default is not None
            )
            if should_print:
                result.append(f"[{name}={param.default!r}]")
            else:
                result.append(f"[{name}]")
        elif param.kind == param.VAR_POSITIONAL:
            result.append(f"[{name}...]")
        else:
            result.append(f"<{name}>")

    return " ".join(result)


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Core commands, these are the miscallaneous commands that don't fit into other categories'"""

    process = psutil.Process()
    process.cpu_percent()

    @commands.command()
    @commands.cooldown(1, 2, commands.cooldowns.BucketType.user)
    async def ping(self, ctx):
        await ctx.send(f'Ping is '
                       f'**{int(self.bot.latency * 1000)} ms**!')

    @commands.command()
    @commands.cooldown(1, 3, commands.cooldowns.BucketType.user)
    async def help(self, ctx, *, command: str = None):
        """Shows help about a command or the bot"""

        try:
            if command is None:
                p = await utils.HelpPaginator.from_bot(ctx)
            else:
                entity = ctx.bot.get_cog(command) or ctx.bot.get_command(command)

                if entity is None:
                    clean = command.replace("@", "@\u200b")
                    return await ctx.send(f'Command or category "{clean}" not found.')
                elif isinstance(entity, commands.Command):
                    p = await utils.HelpPaginator.from_command(ctx, entity)
                else:
                    p = await utils.HelpPaginator.from_cog(ctx, entity)

            await p.paginate()
        except Exception as e:
            await ctx.send(e)

    async def _help(self, ctx, *, entity: str = None):
        chunks = []

        if entity:
            entity = ctx.bot.get_cog(entity) or ctx.bot.get_command(entity)
        if entity is None:
            fmt = (
                "Hello! Here is a list of the sections of commands that I have "
                "(there are a lot of commands so just start with the sections...I know, I'm pretty great)\n"
            )
            fmt += "To use a command's paramaters, you need to know the notation for them:\n"
            fmt += "\t<argument> This means the argument is __**required**__.\n"
            fmt += "\t[argument] This means the argument is __**optional**__.\n"
            fmt += "\t[A|B] This means the it can be __**either A or B**__.\n"
            fmt += "\t[argument...] This means you can have multiple arguments.\n"
            fmt += "\n**Type `{}help section` to get help on a specific section**\n".format(
                ctx.prefix
            )
            fmt += "**CASE MATTERS** Sections are in `Title Case` and commands are in `lower case`\n\n"

            chunks.append(fmt)

            cogs = sorted(ctx.bot.cogs.values(), key=lambda c: c.__class__.__name__)
            for cog in cogs:
                tmp = "**{}**\n".format(cog.__class__.__name__)
                if cog.__doc__:
                    tmp += "\t{}\n".format(cog.__doc__)
                if len(chunks[len(chunks) - 1] + tmp) > 2000:
                    chunks.append(tmp)
                else:
                    chunks[len(chunks) - 1] += tmp
        elif isinstance(entity, (commands.core.Command, commands.core.Group)):
            tmp = "**{}**".format(_command_signature(entity))
            tmp += "\n{}".format(entity.help)
            chunks.append(tmp)
        else:
            cmds = sorted(entity.get_commands(), key=lambda c: c.name)
            fmt = "Here are a list of commands under the section {}\n".format(
                entity.__class__.__name__
            )
            fmt += "Type `{}help command` to get more help on a specific command\n\n".format(
                ctx.prefix
            )

            chunks.append(fmt)

            for command in cmds:
                for subcommand in command.walk_commands():
                    tmp = "**{}**\n\t{}\n".format(
                        subcommand.qualified_name, subcommand.short_doc
                    )
                    if len(chunks[len(chunks) - 1] + tmp) > 2000:
                        chunks.append(tmp)
                    else:
                        chunks[len(chunks) - 1] += tmp

        if utils.dev_server:
            tmp = "\n\nIf I'm having issues, then please visit the dev server and ask for help. {}".format(
                utils.dev_server
            )
            if len(chunks[len(chunks) - 1] + tmp) > 2000:
                chunks.append(tmp)
            else:
                chunks[len(chunks) - 1] += tmp

        if len(chunks) == 1 and len(chunks[0]) < 1000:
            destination = ctx.channel
        else:
            destination = ctx.author

        try:
            for chunk in chunks:
                await destination.send(chunk)
        except (discord.Forbidden, discord.HTTPException):
            await ctx.send(
                "I cannot DM you, please allow DM's from this server to run this command"
            )
        else:
            if ctx.guild and destination == ctx.author:
                await ctx.send("I have just DM'd you some information about me!")

    @commands.command()
    async def calendar(self, ctx, month: str = None, year: int = None):
        """Provides a printout of the current month's calendar
        Provide month and year to print the calendar of that year and month

        EXAMPLE: pbcalendar january 2011"""

        # calendar takes in a number for the month, not the words
        # so we need this dictionary to transform the word to the number
        months = {
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12,
        }
        # In month was not passed, use the current month
        if month is None:
            month = datetime.date.today().month
        else:
            month = months.get(month.lower())
            if month is None:
                await ctx.send("Please provide a valid Month!")
                return
        # If year was not passed, use the current year
        if year is None:
            year = datetime.datetime.today().year
        # Here we create the actual "text" calendar that we are printing
        cal = calendar.TextCalendar().formatmonth(year, month)
        await ctx.send("```\n{}```".format(cal))

    @commands.command(aliases=["invite"])
    async def addbot(self, ctx):
        """Provides a link that you can use to add me to a server

        EXAMPLE: pbaddbot
        RESULT: http://discord.gg/yo_mama"""
        perms = discord.Permissions.none()
        perms.read_messages = True
        perms.send_messages = True
        perms.manage_roles = True
        perms.ban_members = True
        perms.kick_members = True
        perms.manage_messages = True
        perms.embed_links = True
        perms.read_message_history = True
        perms.attach_files = True
        perms.speak = True
        perms.connect = True
        perms.attach_files = True
        perms.add_reactions = True
        app_info = await ctx.bot.application_info()
        await ctx.send(
            "Use this URL to add me to a server that you'd like!\n<{}>".format(
                discord.utils.oauth_url(app_info.id, perms)
            )
        )

    @commands.command()
    async def roll(self, ctx, *, notation: str = "d6"):
        """Rolls a die based on the notation given
        Format should be #d#

        EXAMPLE: pbroll d50
        RESULT: 51 :^)"""
        # Use regex to get the notation based on what was provided
        try:
            # We do not want to try to convert the dice, because we want d# to
            # be a valid notation
            dice = re.search(r"(\d*)d(\d*)", notation).group(1)
            num = int(re.search(r"(\d*)d(\d*)", notation).group(2))
            # Attempt to get addition/subtraction
            add = re.search(r"\+ ?(\d+)", notation)
            subtract = re.search(r"- ?(\d+)", notation)
        # Check if something like ed3 was provided, or something else entirely
        # was provided
        except (AttributeError, ValueError):
            await ctx.send("Please provide the die notation in #d#!")
            return

        # Dice will be None if d# was provided, assume this means 1d#
        dice = dice or 1
        # Since we did not try to convert to int before, do it now after we
        # have it set
        dice = int(dice)
        if dice > 30:
            await ctx.send("I'm not rolling more than 30 dice, I have tiny hands")
            return
        if num > 100:
            await ctx.send("What die has more than 100 sides? Please, calm down")
            return
        if num <= 1:
            await ctx.send(
                "A {} sided die? You know that's impossible right?".format(num)
            )
            return

        nums = [random.SystemRandom().randint(1, num) for _ in range(0, int(dice))]
        subtotal = total = sum(nums)
        # After totalling, if we have add/subtract seperately, apply them
        if add:
            add = int(add.group(1))
            total += add
        if subtract:
            subtract = int(subtract.group(1))
            total -= subtract
        value_str = ", ".join("{}".format(x) for x in nums)

        if dice == 1:
            fmt = "{0.message.author.name} has rolled a {1} sided die and got the number {2}!".format(
                ctx, num, value_str
            )
            if add or subtract:
                fmt += "\nTotal: {} ({}".format(total, subtotal)
                if add:
                    fmt += " + {}".format(add)
                if subtract:
                    fmt += " - {}".format(subtract)
                fmt += ")"
        else:
            fmt = "{0.message.author.name} has rolled {1}, {2} sided dice and got the numbers {3}!".format(
                ctx, dice, num, value_str
            )
            if add or subtract:
                fmt += "\nTotal: {} ({}".format(total, subtotal)
                if add:
                    fmt += " + {}".format(add)
                if subtract:
                    fmt += " - {}".format(subtract)
                fmt += ")"
            else:
                fmt += "\nTotal: {}".format(total)
        await ctx.send(fmt)


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
