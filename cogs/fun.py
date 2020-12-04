import asyncio
import aiohttp
import discord
import json
import praw
import random
import requests

from discord.ext import commands


def setup(bot):
    bot.add_cog(Fun(bot))


agent = praw.Reddit(client_id='Ceva16eRbrWxog',
                    client_secret='0ZaRckgTXapz2D2z1N66UrNJHQQ',
                    user_agent='discord name yakoi#0666',
                    username='PythonBot')


def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="slap", aliases=["hit", 'SLAP', 'HIT'])
    async def slap_member(self, ctx, member: discord.Member, *, reason: str = "for no reason"):
        """
        You slap a user

        EXAMPLE: pbslap @username i love you
        RESULT: @username got slaped by @yourname. reason: i love you
        Command aliases: ['hit']
        """

        if not member or member.id == ctx.author.id:
            await ctx.send(f'{ctx.author.display_name}. Hit him self like an idiot. HAHA DUMB ASS.')
        elif member.bot:
            await ctx.send(f'**BACK OFF MY KIND**')
        else:
            await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}!")

    @commands.command(aliases=['GIF'])
    async def gif(self, ctx, *, search: str = None):
        """Search on a gif sit on random gifs that you want

        EXAMPLE: pbgif hamster
        RESULT: sends a random gif of a hamster
        """
        embed = discord.Embed(colour=discord.Colour.blue(), title=f'You search for "{search}" on GIPHY')
        session = aiohttp.ClientSession()

        if search is None:
            embed = discord.Embed(colour=discord.Colour.blue(), title=f'You search for "random" on GIPHY')
            response = await session.get(
                'https://api.giphy.com/v1/gifs/random?api_key=ha15mc2mmkoPOCCXqzbTnr9SvPRM5PD2&limit=50&rating=PG-13'
                '&lang=eu')
            data = json.loads(await response.text())
            embed.set_image(url=data['data']['images']['original']['url'])
        else:
            search.replace(' ', '+')
            response = await session.get(
                'http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=ha15mc2mmkoPOCCXqzbTnr9SvPRM5PD2&limit'
                                                                    '=50&rating=PG-13&lang=eu')
            data = json.loads(await response.text())
            gif_choice = random.randint(0, 49)
            embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

        await session.close()

        await ctx.send(embed=embed)

    @commands.command(aliases=['ym', 'yomama', 'ymom'])
    async def yomoma(self, ctx):
        """Gives you a random Yomoma joke

        EXAMPLE: pbyomoma
        RESULT: sends a random joke about your mom ;)
        Command aliases: ['ym','yomama','ymom']
        """
        r = requests.get('http://api.yomomma.info/')
        data = json.loads(r.content)
        tjokes = data['joke']

        await ctx.send(tjokes)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['POLL'])
    async def poll(self, ctx, *, args):
        f"""Creates a poll. Takes the polltext as an argument.
        
        EXAMPLE: pbpoll do you guys want to play amongus?\n yes \n no
        RESULT:  do you guys want to play amongus?\n yes\n no
        """
        await ctx.message.delete()
        embed = discord.Embed(title="Poll:", description=args, color=self.bot.config.color)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        embed.set_thumbnail(url=random_line('pollimages'))
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
        await message.add_reaction('👎')
        await message.add_reaction('🤷')

    @commands.command(name='meme', aliases=['MEME', 'MEMES', 'memes'])
    async def _meme(self, ctx):
        """
        sends a meme

        EXAMPLE: pbmeme
        RESULT: sends a random meme
        Command aliases: ['memes']
        """
        memes_submissions = agent.subreddit('dankmemes').top()
        post_to_pick = random.randint(0, 50)

        for i in range(post_to_pick):
            self.subs1 = next(x for x in memes_submissions if not x.stickied)

        embed = discord.Embed(colour=discord.Colour.red(), title=f"**{self.subs1.title}**", url=self.subs1.url)
        embed.set_image(url=self.subs1.url)
        embed.set_footer(text=f'👍 {self.subs1.ups}  |  💬 {self.subs1.num_comments}')

        await ctx.send(embed=embed)

    @commands.command(aliases=['BOOBS'])
    @commands.is_nsfw()
    async def boobs(self, ctx):

        memes_submissions = agent.subreddit('boobs').top()
        post_to_pick = random.randint(0, 50)

        for i in range(post_to_pick):
            self.subs2 = next(x for x in memes_submissions if not x.stickied)

        embed = discord.Embed(colour=discord.Colour.red(), title=f"**{self.subs2.title}**", url=self.subs2.url)
        embed.set_image(url=self.subs2.url)
        embed.set_footer(text=f'👍 {self.subs2.ups}  |  💬 {self.subs2.num_comments}')

        await ctx.send(embed=embed)

    @commands.command(aliases=['ASS'])
    @commands.is_nsfw()
    async def ass(self, ctx):
        memes_submissions = agent.subreddit('ass').top()
        post_to_pick = random.randint(0, 50)

        for i in range(post_to_pick):
            self.subs3 = next(x for x in memes_submissions if not x.stickied)

        embed = discord.Embed(colour=discord.Colour.red(), title=f"**{self.subs3.title}**", url=self.subs3.url)
        embed.set_image(url=self.subs3.url)
        embed.set_footer(text=f'👍 {self.subs3.ups}  |  💬 {self.subs3.num_comments}')

        await ctx.send(embed=embed)

    @commands.command(aliases=['PUSSY'])
    @commands.is_nsfw()
    async def pussy(self, ctx):
        memes_submissions = agent.subreddit('pussy').top()
        post_to_pick = random.randint(0, 50)

        for i in range(post_to_pick):
            self.subs4 = next(x for x in memes_submissions if not x.stickied)

        embed = discord.Embed(colour=discord.Colour.red(), title=f"**{self.subs4.title}**", url=self.subs4.url)
        embed.set_image(url=self.subs4.url)
        embed.set_footer(text=f'👍 {self.subs4.ups}  |  💬 {self.subs4.num_comments}')

        await ctx.send(embed=embed)

    @commands.command(aliases=['Reddit', 'rt', 'RT'])
    @commands.is_allowed()
    async def reddit(self, ctx, *, memez):
        """Search on reddit

        EXAMPLE: pbreddit ksi
        RESULT: sends a random thing from r/ksi
        Command aliases: ['Reddit', 'rt']
        Access only: Trusted
        """

        memes_submissions = agent.subreddit(memez).top()
        post_to_pick = random.randint(0, 50)

        for i in range(post_to_pick):
            self.subs5 = next(x for x in memes_submissions if not x.stickied)

        embed = discord.Embed(colour=discord.Colour.red(), title=f"**{self.subs5.title}**", url=self.subs5.url)
        embed.set_image(url=self.subs5.url)
        embed.set_footer(text=f'👍 {self.subs5.ups}  |  💬 {self.subs5.num_comments}')

        await ctx.send(embed=embed)

    @commands.command(name="8ball", aliases=['8BALL'])
    async def _8ball(self, ctx, *, question):
        """
        Its a 8ball command. What do you want to know?

        EXAMPLE: pb8ball should i buy amongus?
        RESULT: gives you a random responses could be no or go fuck your self
        """
        fuckyou = ['fuck you', 'FUCK YOU']
        python = ['python', 'PYTHON', 'py']
        if question in python:
            responses = [
                'Ask Gustav',
                'PYTHON IS THE BEST',
                'C# is trash',
                'C# users should programme in python',
                'python is good',
            ]
        elif question in fuckyou:
            responses = ['NO FUCK YOU', 'GO FUCK YOURSELF IDIOT']
        else:
            responses = [
                'As I see it, yes.',
                'Ask again later.',
                'Better not tell you now.',
                'Cannot predict now.',
                'Concentrate and ask again.',
                'Don’t count on it.',
                'It is certain.',
                'It is decidedly so.',
                'Most likely.',
                'My reply is no.',
                'My sources say no.',
                'Outlook not so good.',
                'Outlook good.',
                'Reply hazy, try again.',
                'Signs point to yes.',
                'Very doubtful.',
                'Without a doubt.',
                'Yes.',
                'Yes – definitely.',
                'You may rely on it.',
                "I don't know. Ask yourself",
                'WHAT THE FUCK DO YOU WANT FROM ME YOU FUCK HEAD?',
                'Fuck off',
                'Cunt',
                "Sorry i don't know :(",
                'Having a bad day?',
                'Sure',
            ]
        await ctx.send(f'Question: {question}\nMy answer: {random.choice(responses)}')

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['flip', 'coin', 'cf', 'CF', 'COINFLIP'])
    async def coinflip(self, ctx, user: discord.Member = None):
        """ Flip a coin!


        EXAMPLE: pbcoinflip or pbcoinflip @username
        RESULT: if you do pbcoinflip you well get a random head or tails
        if you @username then @username is allways tails and the one who send the msg is heads Command aliases: [
        'flip', 'coin', 'cf']
        """
        coinsides = ['Heads', 'Tails']
        if user is None:
            return await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

        p1 = user.name
        p2 = ctx.author.name

        winner = random.choice(coinsides)
        if winner == 'Heads':
            return await ctx.send(f"**{p2}** flipped **{winner}** and won the Coinflip")
        else:
            return await ctx.send(f"**{p1}** flipped **{winner}** and won the Coinflip")

    @commands.command(aliases=['F'])
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect

        EXAMPLE: pbf
        RESULT: @username has paid their respect
        """

        def is_me(m):
            return m.author == ctx.author

        await ctx.message.channel.purge(limit=1, check=is_me)
        hearts = ['❤', '💛', '💚', '💙', '💜']
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.is_owner()
    async def viktor(self, ctx):
        """Its a meme between owner and the other guy :D

        EXAMPLE: pbviktor
        RESULT: sends a gif of a guy with long dick
        Access only: owner
        """
        await ctx.send('https://media.discordapp.net/attachments/547097300527349775/547576100792827915/video.gif')

    @commands.command(aliases=['BEER'])
    async def beer(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Give someone a beer! 🍻


        EXAMPLE: pbbeer or pbbeer @username
        RESULT: if your lonly and do pbbeer then you get to party by your self.
        Else if you have friends do pbbeer @username if thay respond to the beer icon you well have a lovly beer
        """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("*drinks beer with you* 🍻")
        if user.bot:
            return await ctx.send(
                f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to "
                f"you :/")

        beer_offer = f"**{user.name}**, you got a 🍺 offer from **{ctx.author.name}**"
        beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for('raw_reaction_add', timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** :(")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.command(aliases=['CHUG'])
    async def chug(self, ctx, user: discord.Member = None):
        """
        chugtest XD :D        """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("*Chugging beer with you* 🍻")
        if user.bot:
            return await ctx.send(f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it "
                                  f"will respond to you :/")

        p1 = user.name
        p2 = ctx.author.name
        chug_offer = f"**{p1}**, send you a chugging contest 🍺 **{p2}**"
        msg = await ctx.send(chug_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for('raw_reaction_add', timeout=30.0, check=reaction_check)
            winner = random.randint(1, 2)
            if winner == 1:
                await msg.edit(content=f"**{p1} won the chugtest**")
            else:
                await msg.edit(content=f"**{p2} won the chugtest**")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, doesn't seem like **{p1}** wanted to compete with you **{p2}** what a wus")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            chug_offer = f"**{p1}**, you got a 🍺 from **{p2}**"
            await msg.edit(content=chug_offer)
