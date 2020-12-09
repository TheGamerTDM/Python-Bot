from discord.ext import commands

from utils import exceptions


def dj_only():
    async def predicate(ctx):
        guild = await ctx.bot.guild_cache.get(ctx.guild.id)
        if guild.dj_mode is False:
            return True
        if check_owner(ctx):
            return True
        if ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_guild:
            return True
        if "dj" in [y.name.lower() for y in ctx.author.roles]:
            return True
        raise exceptions.DjOnlyException

    return commands.check(predicate)


def admin_only():
    async def predicate(ctx):
        if check_owner(ctx):
            return True
        if ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_guild:
            return True
        raise exceptions.AdminOnlyException

    return commands.check(predicate)


def owner_only():
    async def predicate(ctx):
        if check_owner(ctx):
            return True
        raise exceptions.OwnerOnlyException

    return commands.check(predicate)


def check_owner(ctx):
    return ctx.author.id in ctx.bot.get_config()['owners']


def premium_only(pledge):
    async def predicate(ctx):
        if check_owner(ctx):
            return True
        async with ctx.bot.get_postgre_client().get_pool().acquire() as connection:
            statement = await connection.prepare('SELECT type FROM premium WHERE user_id = $1')
            patron_type = await statement.fetchval(ctx.author.id)
            if patron_type is None or patron_type < pledge:
                raise exceptions.PremiumOnlyException(pledge)

            return True

    return commands.check(predicate)


async def get_premium_type(user_id, pool):
    async with pool.acquire() as connection:
        check = await connection.prepare('SELECT type FROM premium WHERE user_id = $1')
        final_check = await check.fetchval(user_id)
        return final_check