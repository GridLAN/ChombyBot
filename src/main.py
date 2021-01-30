import os
import logging
import asyncio
import discord
import youtube_dl
import ctypes
import ctypes.util
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

logger.info('ctypes - Find Opus:')
a = ctypes.util.find_library('opus')
logger.info(a)

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]
        
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Dog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def find( self, ctx):
        users = ctx.guild.voice_channels

        userlist = []
        for user in users:
            for u in user.members:
                print(u.name)

    @commands.command()
    async def sic(self, ctx, member: discord.Member):
        """ @ a user to sic Chomby on them"""

        try:
            voice_channel = member.voice.channel

            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(voice_channel)
            await voice_channel.connect()
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('chomby_audio/sic.mp3'))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)

            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
        except:
            await ctx.send("User not in a voice channel")

    @commands.command(help="Call Chomby over")
    async def chomby(self, ctx, *, query='chomby_audio/bark2.wav'):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)

        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(help="Give Chomby a snack")
    async def feed(self, ctx, *, query='chomby_audio/feeding.mp3'):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)

        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(help="Give Chomby a snack")
    async def snore(self, ctx, *, query='chomby_audio/snore.mp3'):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(help="Someone just rang the doorbell..")
    async def dingdong(self, ctx, *, query='chomby_audio/dingdong.mp3'):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)

        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command()
    async def baddog(self, ctx, *, query='chomby_audio/whine.wav'):
        """Sad Chomby"""
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)

        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send("bitch")


    @commands.command()
    async def whistle(self, ctx):
        """Call Chomby"""

        await ctx.channel.connect()

    @commands.command()
    async def crate(self, ctx):
        """Put Chomby in their crate"""

        ctx.voice_channel.stop()
        await ctx.voice_client.disconnect()

    @commands.command()
    async def fetch(self, ctx, *, url):
        '''Chomby will fetch a youtube url'''

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @whistle.before_invoke
    @chomby.before_invoke
    @snore.before_invoke
    @feed.before_invoke
    @dingdong.before_invoke
    @baddog.before_invoke
    @crate.before_invoke
    @fetch.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Not in a voice channel")



class Chomby(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or('..'), description="It's Chomby!", intents=intents)



@bot.event
async def on_ready():
    logger.info('{0} is ready'.format(bot.user))
    print('{0} is ready'.format(bot.user))

@bot.event
async def on_disconnect():
    logger.info('Bot has disconnected')

@bot.event
async def on_error(event, *args, **kwargs):
    logger.info('ERROR: {}'.format(event))

bot.add_cog(Dog(bot))

bot.run(os.getenv('TOKEN'))
