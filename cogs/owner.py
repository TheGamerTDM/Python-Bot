from discord.ext import commands
from git import Repo
from datetime import datetime
import os


@commands.is_owner()
class OwnerCog(commands.Cog, command_attrs=dict(hidden=False), name="Owner"):
    """Commands meant for the owner only."""

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command(name='OwnerDelete', aliases=['odel'])
    @commands.is_owner()
    async def odel(self, ctx, count: int):
        """Owner Delete :D"""
        await ctx.message.channel.purge(limit=count + 1, bulk=True)

    @commands.command(name='reload')
    @commands.is_owner()
    async def _reload(self, ctx, *, module: str):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('DONE :D')
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(name='pull')
    @commands.is_owner()
    async def git_update(self, ctx):
        """Pulls the bot from GitHub."""
        now = datetime.now()
        message = ""
        repo = Repo(path=os.getcwd())
        o = repo.remotes.origin
        for fetch_info in o.pull():
            message = message + f"\n Updated '{fetch_info.ref}' To '{fetch_info.commit}'"
        later = datetime.now()
        difference = (later - now).total_seconds()
        await ctx.send(f"Operation completed succesfully in {difference}s. Output: ```prolog\n{message}\n```")

    @commands.command()
    @commands.is_owner()
    async def shoutdown(self, ctx):
        """Shuts the bot down."""
        await ctx.send("Goodbye!")
        await self.bot.logout()


def setup(bot):
    bot.add_cog(OwnerCog(bot))
