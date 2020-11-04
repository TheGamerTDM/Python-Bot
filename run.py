import sys
import traceback

from classes.bot import PythonBot
import asyncio, os, discord, pyfiglet, time

bot = PythonBot(description='Python Bot', activity=discord.Game(name='my dick'))

try:
    import sentry_sdk

    sentry_sdk.init(bot.config.sentry)
except ImportError:
    print("[Python bot] Failed to initialize sentry.")


def list_module(directory):
    return (f for f in os.listdir(directory) if f.endswith('.py'))


@bot.command()
async def aboutme(ctx):
    await ctx.send(f"This is a bot for fun that im making. Owner: (Yakoi#4895). I love programing and this bot is "
                   f"made 100% with python")


@bot.command()
async def ping(ctx):
    """Ping command."""
    t1 = time.perf_counter()
    await ctx.trigger_typing()
    t2 = time.perf_counter()
    await ctx.send(f"Ping: {round((t2 - t1) * 1000)} ms")


@bot.listen('on_ready')
async def on_ready():
    f = pyfiglet.Figlet()
    print(f.renderText(bot.config.splashArt))
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    print(f'Successfully logged in and booted...!')
    try:
        bot.load_extension('music')
    except:
        pass
    # Load Modules
    module_folders = ['listeners', 'cogs']
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
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run())
    except KeyboardInterrupt:
        print("Stopping bot!")
