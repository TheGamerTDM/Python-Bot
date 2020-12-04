import discord
from discord.ext import commands


@commands.is_allowed()
class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        await ctx.send(f'{user.status}')

    # @commands.command(name="serverstats", aliases=["si", "ss", "check-stats", 'cs'])
    # async def serverstats(self, ctx: commands.Context):
    #     embed = discord.Embed(
    #         color=discord.Colour.orange(),
    #         title=f"{ctx.guild.name}")
    #
    #     embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    #     embed.add_field(name="👑Owner", value=f"<@{ctx.message.guild.owner_id}>", inline=False)
    #     embed.add_field(name="🌍Region", value=f"{ctx.guild.region}")
    #     embed.add_field(name="👥Member's", value=f"{ctx.guild.member_count}")
    #     embed.add_field(name="🤣Emoji's", value=f"{len(ctx.guild.emojis)}")
    #     embed.add_field(name="🧻Roles", value=f"{len(ctx.guild.roles)}")
    #     embed.add_field(name="📄Text Channel", value=f"{len(ctx.guild.text_channels)}")
    #     embed.add_field(name="📆Created at", value=f"{ctx.guild.created_at.date()}")
    #     embed.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"Requested by {ctx.author.name}")
    #
    #     await ctx.send(embed=embed)

    @commands.command(aliases=['ui'])
    async def userstats(self, ctx, *, user: discord.Member = None):
        """Provides information about a provided member
        EXAMPLE: !userinfo
        RESULT: Information about yourself!"""
        if user is None:
            user = ctx.message.author

        embed = discord.Embed(color=discord.Colour.orange())
        fmt = "{} ({})".format(str(user), user.id)
        embed.set_author(name=fmt, icon_url=user.avatar_url)

        embed.add_field(
            name="Joined this server", value=user.joined_at.date(), inline=False
        )
        embed.add_field(
            name="Joined Discord", value=user.created_at.date(), inline=False
        )

        # # Sort them based on the hierarchy, but don't include @everyone
        # roles = sorted([x for x in user.roles if not x.is_default()], reverse=True)
        # # I only want the top 5 roles for this purpose
        # roles = ", ".join("{}".format(x.name) for x in roles[:5])
        # # If there are no roles, then just say this
        # roles = roles or "No roles added"
        # embed.add_field(name="Top 5 roles", value=roles, inline=False)
        #
        # Add the activity if there is one
        act = user.activity
        if isinstance(act, discord.activity.Spotify):
            embed.add_field(name="Listening to", value=act.title, inline=False)
        elif isinstance(act, discord.activity.Game):
            embed.add_field(name="Playing", value=act.name, inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['ut'])
    async def usertest(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        if user.activity is not None:
            game = user.activity
        else:
            game = None
        voice_state = None if not user.voice else user.voice.channel
        embed = discord.Embed(timestamp=ctx.message.created_at, colour=self.bot.config.color)
        embed_values = {
            "User ID": user.id,
            "Nick": user.nick,
            "Status": user.status,
            "In Voice": voice_state,
            "Game": game,
            "Highest Role": user.top_role.name,
            "Account Created": user.created_at.date(),
            "Join Date": user.joined_at.date()
        }
        for n, v in embed_values.items():
            embed.add_field(name=n, value=v, inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)







def setup(bot):
    bot.add_cog(Test(bot))
