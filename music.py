import re
from asyncio import sleep
import discord
from discord.ext import commands
import lavalink
import math

url_rx = re.compile(r'https?://(?:www\.)?.+')
time_rx = re.compile('[0-9]+')


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pause = True
        self.request = []

        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node('localhost', 7000, 'testing', 'eu',
                                  'music-node')  # Host, Port, Password, Region, Name
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None

        if guild_check:
            await self.ensure_voice(ctx)

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))

        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('Join a voicechannel first.')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voicechannel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voicechannel ID. A channel_id of `None` means disconnect. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.command(aliases=['p', 'PLAY', 'Play', 'P'])
    async def play(self, ctx, *, query: str = None):
        """ Searches and plays a song from a given query. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not self.pause:
            await player.set_pause(False)
            await ctx.send(f'▶ **Resuming**')
            self.pause = True
        elif query is None:
            await ctx.send(f'**Pleas type some thing or paste a url**')
        else:
            await ctx.send(f'**Searching**🔎 `{query}`.')
            query = query.strip('<>')

            if not url_rx.match(query):
                query = f'ytsearch:{query}'

            results = await player.node.get_tracks(query)

            if not results or not results['tracks']:
                return await ctx.send('Nothing found!')

            # Valid loadTypes are:
            #   TRACK_LOADED    - single video/direct URL)
            #   PLAYLIST_LOADED - direct URL to playlist)
            #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
            #   NO_MATCHES      - query yielded no results
            #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
            await sleep(0.5)
            if results['loadType'] == 'PLAYLIST_LOADED':
                tracks = results['tracks']


                for track in tracks:
                    player.add(requester=ctx.author.id, track=track)

                await ctx.send(
                    f'**Queueing up** 🎶 `{results["playlistInfo"]["name"]} - {len(tracks)}` - Now! Requested by: {ctx.author}')
            else:
                track = results['tracks'][0]
                await ctx.send(f'**Queueing up** 🎶 `{track["info"]["title"]}` - Now! Requested by: {ctx.author}')

                track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
                player.add(requester=ctx.author.id, track=track)

            if not player.is_playing:
                await player.play()

    @commands.command(aliases=['forceskip', 'fs'])
    async def skip(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Not playing.')

        await ctx.send(f'⏩ ***skipped***.')
        await player.skip()

    @commands.command(aliases=['qc', 'QC'])
    async def queueclear(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Not playing.')
        player.queue.clear()
        await ctx.send('👌 cleared the queue.')

    @commands.command(aliases=['stop', 'STOP', 'PAUSE', 'Stop', 'Pause'])
    async def pause(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Not playing.')

        if self.pause:
            await player.set_pause(True)
            await ctx.send(f'**Paused** ⏸')
            self.pause = False

    @commands.command(aliases=['dc', 'Disconnect', 'DC', 'DISCONNECT'])
    async def disconnect(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voicechannel!')

        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        await ctx.send(f'<:pepebigcry:767628237546192926> **Successfully disconnected**')

    @commands.command(aliases=['q', 'Q''QUEUE', 'Queue'])
    async def queue(self, ctx, page: int = 1):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send('There\'s nothing in the queue! Why not queue something?')

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page
        duration = lavalink.utils.format_time(player.current.duration)
        queue_list = ''
        for i, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{i + 1}.` [**{track.title}**]({track.uri})\n'

        embed = discord.Embed(colour=ctx.guild.me.top_role.colour,
                              title='Queue list',
                              description=f'{queue_list}')

        embed.set_footer(
            # icon_url=f'{ctx.message.author.avatar_url}',
            text=f'\n {len(player.queue)} tracks \n page {page}/{pages}')

        await ctx.send(embed=embed)

    @commands.command(aliases=['np', 'N', 'n', 'playing'])
    async def now(self, ctx):
        """ Shows some stats about the currently playing song. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.current:
            return await ctx.send('Nothing playing.')

        position = lavalink.utils.format_time(player.position)
        if player.current.stream:
            duration = '🔴 LIVE'
        else:
            duration = lavalink.utils.format_time(player.current.duration)
        song = f'**[{player.current.title}]({player.current.uri})**\n({position}/{duration})'

        embed = discord.Embed(colour=ctx.guild.me.top_role.colour,
                              title='Now Playing', description=song)
        await ctx.send(embed=embed)

    @commands.command(aliases=['SEEK', 'Seek'])
    async def seek(self, ctx, *, seconds: int):
        """ Seeks to a given position in a track. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        track_time = player.position + (seconds * 1000)
        await player.seek(track_time)

        await ctx.send(f'Moved track to **{lavalink.utils.format_time(track_time)}**')

    @commands.command(aliases=['vol', 'VOL', 'Vol'])
    async def volume(self, ctx, volume: int = None):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not volume:
            return await ctx.send(f'🔈 | {player.volume}%')

        await player.set_volume(volume)
        await ctx.send(f'🔈 | Set to {player.volume}%')

    @commands.command(aliases=['rep', 'REP', 'Rep'])
    async def repeat(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Nothing playing.')

        player.repeat = not player.repeat

        await ctx.send('🔁 | Repeat ' + ('enabled' if player.repeat else 'disabled'))


def setup(bot):
    bot.add_cog(Music(bot))
