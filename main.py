import time
import discord
import asyncio
import os
import sys
import traceback
from classes.bot import PythonBot
from discord.ext import commands
import utils

intent = discord.Intents.all()
intent.presences = False

opts = {
    "description": 'Python Bot',
    "command_not_found": "",
    "activity": discord.Game(name='pbhelp for help :D'),
    "allowed_mentions": discord.AllowedMentions(everyone=False),
    "intents": intent,
    "help_command": None,
    "chunk_guilds_at_startup": False,
    "guild_subscriptions": True,
}

bot = PythonBot(**opts, case_insensitive=True)

try:
    import sentry_sdk

    sentry_sdk.init(bot.config.sentry)
except ImportError:
    print("[Python bot] Failed to initialize sentry.")


def list_module(directory):
    return (f for f in os.listdir(directory) if f.endswith('.py'))


@bot.event
async def on_ready():
    print(f'{bot.user.name}')

    # Load Modules
    module_folders = ['cogs']
    for module in module_folders:
        for extension in list_module(module):
            try:
                bot.load_extension(f'{module}.{os.path.splitext(extension)[0]}')
            except Exception:
                print(f'Failed to load module {module}.{os.path.splitext(extension)[0]}.', file=sys.stderr)
                traceback.print_exc()


async def run():
    await bot.start(bot.config.token, bot=True, reconnect=True)


if __name__ == '__main__':
    bot.remove_command("help")

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run())
    except KeyboardInterrupt:
        print("Stopping bot!")
