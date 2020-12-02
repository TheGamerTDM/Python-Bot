import random
import discord
import asyncio
from time import sleep
from discord.ext import commands


def setup(bot):
    bot.add_cog(fight(bot))


class figherfuckers():
    def __init__(self, user: discord.Member):
        self.id = user.id
        self.user = user
        self.health = 100
        self.armor = 0


@commands.is_owner()
class fight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='fight')
    async def _fight(self, ctx, user: discord.Member):
        """Im working on this its not done yet"""
        print('yes1')
        author = figherfuckers(ctx.author)
        enemy = figherfuckers(user)

        if not enemy:
            return await ctx.send(f'you need to provide a valid user ID or name to fight against lol')
        if enemy.id == author.id:
            return await ctx.send(f'You can\'t fight urself dumbo')
        if ctx.author.bot:
            return await ctx.send(f'You can\'t fight against bots, you\'ll never hear back from them u dummy')
        print('yes2')
        enemy.health = author.health = 100
        enemy.armor = author.armor = 0

        self.turn = author
        self.oppturn = enemy
        print('yes3')

        if random.randint(1, 100) >= 50:
            self.oppturn, self.turn = [self.turn, self.oppturn]
        print('yes4')

        async def performTurn(attacker, opponent, retry):
            print('yes5')
            await ctx.send(
                f'{self.turn.mention}, what do you want to do? `punch`, `defend` or `end``?\nType your choice '
                f'out in chat as it\'s displayed!')
            prompt = await ctx.MessageCollector.awaitMessage(ctx.channel.id, attacker.id, 30e3)
            if not prompt:
                await ctx.send(f'{attacker.name} didn\'t answer in time, what a noob. {opponent} wins')
            elif prompt.content.toLowerCase() == 'punch':
                critChance = random.randint(1, 100) >= 75  # 25 % chance
                damage = random.randint(1, 85 if critChance else 65)

                opponent.health -= 5 if (damage - opponent.armor < 0) else damage - opponent.armor
                return damage
            elif prompt.content.toLowerCase() == 'defend':
                critChance = random.randint(1, 100) >= 75  # 25 % chance
                defense = random.randint(5, 40 if critChance else 20)

                if attacker.armor < 50:
                    attacker.armor += defense
                    await ctx.send(
                        f'**{attacker.name}** increased their protec level by **{defense}**! THEY PROTEC')
                else:
                    await ctx.send(f'don\'t be greedy ur already at the max armor level')
                return False
            elif prompt.content.toLowerCase() == 'end':
                await ctx.send(f'**{attacker.name}** has ended the game what a wimp')
            else:
                await ctx.send(
                    f'**{attacker.name}**, that\'s not a valid option lmao! You must type \`punch\`, \`defend\` or \`end\` in chat!\n {retry}? The game has ended due to multiple invalid choices, god ur dumb')
                if not retry:
                    return performTurn(attacker, opponent, True)
            print('yes6')

        async def play():
            damage = await performTurn(self.turn, self.oppturn)
            if damage is None:
                return
            if not damage:
                self.oppturn, self.turn = [self.turn, self.oppturn]
                return play()
            print('yes7')

            adjective = random.choice(
                ['an incredible', 'a dank', 'a l33t', 'a game-ending', 'an amazing', 'a dangerous', 'a painful',
                 'a CrAzY'])

            await ctx.send(f'**{self.turn.name}** lands {adjective} hit on **{self.oppturn.name}** dealing **{damage}**!\n **{self.oppturn.name}** is left with {0 if self.oppturn.health < 0 else self.oppturn.health} health!')
            print('yes8')

            if self.turn.health > 0 and self.oppturn.health > 0:
                self.oppturn, self.turn = [self.turn, self.oppturn]
                return play()
            else:
                if self.turn.health > 1:
                    loser = self.turn
                else:
                    loser = self.oppturn

                winner = loser
                loser.health = 0

                wowword = random.choice(
                    ['Holy heck!', 'Wow!', 'I did not expect that!', 'Like it or hate it,', 'YES!', 'This is so sad!',
                     'very good', 'Dang!'])
                noun = random.choice(
                    ['just', 'totally', 'heckin', '100%', 'absolutely', 'fricken', 'legitimately', 'completely'])
                verb = random.choice(
                    ['rekt', 'beaned', 'memed', 'destroyed', 'hecked', 'ruined', 'bamboozled', 'roasted'])

                await ctx.send(f'{wowword} **{winner.name}** {noun} {verb} **{loser.name}**, winning with just `{winner.health} HP` left!')
            print('yes9')

        await play()
