import random
import discord
import asyncio
from time import sleep
from discord.ext import commands

def setup(bot):
    bot.add_cog(fighttest(bot))

class fighttest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fight(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """Im working on this its not done yet"""
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: you cant fight your self")
        if user.id == self.bot.user.id:
            return await ctx.send("You can't fight me idiot")
        if user.bot:
            return await ctx.send(f"You cant fight other bots sorry. I don't think it will respond to you :/")

        fight_offer = f"**{user.name}**, you got a fight offer from **{ctx.author.name}**"
        fight_offer = fight_offer + "\n\n**Reason:** {reason}" if reason else fight_offer
        msg = await ctx.send(fight_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🥊":
                return True
            return False

        try:
            await msg.add_reaction("🥊")
            await self.bot.wait_for('raw_reaction_add', timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are in a fight know")
            sleep(2)
            await msg.delete()
            await ctx.send(f"**{ctx.author.name}**, what do you want to do? `Punch`, `Defend`or `End`?\nType your "
                           f"choice out in chat as it's displayed!")
            health = 100
            if ctx.author.send == 'Punch':
                minus_health = health - random.randint(1, 30)
                await ctx.send(f"**{user.name}** lost {minus_health} health")



        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, doesn't seem like **{user.name}** wanted to fight you **{ctx.author.name}**. PUSSY")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            fight_offer = f"**{user.name}**, you got a fight offer from **{ctx.author.name}**"
            await msg.edit(content=fight_offer)
