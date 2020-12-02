import discord
from discord.ext import commands


class Information(commands.Cog):
    """Retrieve information about various items."""

    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def userinfo(self, ctx, user: discord.Member = None):
        """
        Gives you userinfo about your self or others

        EXAMPLE: pbuserinfo or pbuserinfo @username
        RESULT: 1. Get info about your self. 2. Get info about @username
        """
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

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name="serverinfo", aliases=["si", "ss", "check-stats", 'cs'])
    async def _serverstats(self, ctx: commands.Context):
        """
        Get serverinfo

        EXAMPLE: pbserverinfo
        RESULT: Get server info
        """
        embed = discord.Embed(
            color=discord.Colour.orange(),
            title=f"{ctx.guild.name}")

        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        embed.add_field(name="👑Owner", value=f"<@{ctx.message.guild.owner_id}>", inline=False)
        embed.add_field(name="🌍Region", value=f"{ctx.guild.region}")
        embed.add_field(name="👥Member's", value=f"{ctx.guild.member_count}")
        embed.add_field(name="🤣Emoji's", value=f"{len(ctx.guild.emojis)}")
        embed.add_field(name="🧻Roles", value=f"{len(ctx.guild.roles)}")
        embed.add_field(name="📄Text Channel", value=f"{len(ctx.guild.text_channels)}")
        embed.add_field(name="📆Created at", value=f"{ctx.guild.created_at.date()}")
        embed.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
