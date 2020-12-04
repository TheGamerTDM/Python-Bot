from asyncio import sleep
import discord
from discord.ext import commands


class Admin(commands.Cog):
    """Commands for managing Discord servers."""

    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['SPAM'])
    @commands.has_permissions(manage_messages=True)
    async def spam(self, ctx, times: int, *, content='repeating...'):
        """Spam as much as you want (Max 100)

        EXAMPLE: pbspam 5 i love you mom
        RESULT: (i love you mom) x 5
        """
        await ctx.message.channel.purge(limit=1)
        if times <= 100:
            for i in range(times):
                await ctx.send(content)
        else:
            await ctx.send(f'Under 100 please. U {times}')

    @commands.command(aliases=['SEND'])
    @commands.has_permissions(manage_messages=True)
    async def send(self, channel, *, content):
        """Send a message to a channel

        EXAMPLE: pbsend #chat how are you guys
        RESULT: in #chat how are you guys
        """
        if "#" in channel:
            channel = self.bot.get_channel(int(channel[2:-1]))
            await channel.send(content)
        else:
            channel = self.bot.get_channel(int(channel))
            await channel.send(content)

    @commands.command(aliases=['KICK'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member):
        """Kicks a user from the server.

        EXAMPLE: pbkick @username
        RESULT: @username kicked from the server
        """
        if ctx.author == user:
            await ctx.send("You cannot kick yourself.")
        else:
            await user.kick()
            embed = discord.Embed(title=f'User {user.name} has been kicked.', color=0x00ff00)
            embed.add_field(name="Goodbye!", value=":boot:")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(aliases=['BAN'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member):
        """Bans a user from the server.

        EXAMPLE: pbban @username
        RESULT: @username bande from the server
        """
        if ctx.author == user:
            await ctx.send("You cannot ban yourself.")
        else:
            await user.ban()
            embed = discord.Embed(title=f'User {user.name} has been banned.', color=0x00ff00)
            embed.add_field(name="Goodbye!", value=":hammer:")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(aliases=['MUTE'])
    @commands.has_permissions(manage_channels=True)
    async def mute(self, ctx, user: discord.Member, time: int):
        """Prevents a user from speaking for a specified amount of time.

        EXAMPLE: pbmute @username 120
        RESULT: @username gets muted for 120 sec
        """
        if ctx.author == user:
            await ctx.send("You cannot mute yourself.")
        else:
            rolem = discord.utils.get(ctx.message.guild.roles, name='Muted')
            if rolem is None:
                embed = discord.Embed(title="Muted role",
                                      url="http://echo-bot.wikia.com/wiki/Setting_up_the_muted_role",
                                      description="The mute command requires a role named 'Muted'.", color=0xff0000)
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                embed.set_footer(text="Without this role, the command will not work.")
                await ctx.send(embed=embed)
            elif rolem not in user.roles:
                embed = discord.Embed(title=f'User {user.name} has been successfully muted for {time}s.',
                                      color=0x00ff00)
                embed.add_field(name="Shhh!", value=":zipper_mouth:")
                embed.set_thumbnail(url=user.avatar_url)
                await ctx.send(embed=embed)
                await user.add_roles(rolem)
                await sleep(time)
                if rolem in user.roles:
                    try:
                        await user.remove_roles(rolem)
                        embed = discord.Embed(title=f'User {user.name} has been automatically unmuted.', color=0x00ff00)
                        embed.add_field(name="Welcome back!", value=":open_mouth:")
                        embed.set_thumbnail(url=user.avatar_url)
                        await ctx.send(embed=embed)
                    except Exception:
                        print(f'User {user.name} could not be unmuted!')
            else:
                await ctx.send(f'User {user.mention} is already muted.')

    @commands.command(aliases=['UNMUTE'])
    @commands.has_permissions(manage_channels=True)
    async def unmute(self, ctx, user: discord.Member):
        """Unmutes a user.

        EXAMPLE: pbunmute @username
        RESULT: @username gets unmutede
        """
        rolem = discord.utils.get(ctx.message.guild.roles, name='Muted')
        if rolem in user.roles:
            embed = discord.Embed(title=f'User {user.name} has been manually unmuted.', color=0x00ff00)
            embed.add_field(name="Welcome back!", value=":open_mouth:")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)
            await user.remove_roles(rolem)

    @commands.command(name='remove', aliases=['dump', 'rm', 'clear', 'REMOVE', 'RM'])
    @commands.has_permissions(manage_messages=True)
    async def prune(self, ctx, count: int = 1):
        """Deletes a specified amount of messages. (Max 100)

        EXAMPLE: pbpurne 50
        RESULT: delets 50 msg in that channel
        Command aliases: ['dump', 'rm', 'clear']
        """
        if count > 100:
            count = 100
        await ctx.message.channel.purge(limit=count + 1, bulk=True)

    @commands.command(aliases=['CLEAN'])
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx):
        """Cleans the chat of the bot's messages.

        EXAMPLE: pbclean
        RESULT: it removes what the bot have sendt. 100 at a time
        """

        def is_me(m):
            return m.author == self.bot.user

        await ctx.message.channel.purge(limit=100, check=is_me)


def setup(bot):
    bot.add_cog(Admin(bot))
