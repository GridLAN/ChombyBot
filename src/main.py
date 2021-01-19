import os
import asyncio
import discord
from discord.ext import commands

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
            ctx.voice_client.play(source)

            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)

            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
        except:
            await ctx.send("User not in a voice channel")

    @commands.command(help="Call Chomby over")
    async def chomby(self, ctx, *, query='chomby_audio/bark2.wav'):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(help="Give Chomby a snack")
    async def feed(self, ctx, *, query='chomby_audio/feeding.mp3'):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(help="Give Chomby a snack")
    async def snore(self, ctx, *, query='chomby_audio/snore.mp3'):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(help="Someone just rang the doorbell..")
    async def dingdong(self, ctx, *, query='chomby_audio/dingdong.mp3'):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)

        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
    
    @commands.command()
    async def baddog(self, ctx, *, query='chomby_audio/whine.wav'):
        """Sad Chomby"""
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)

        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send("bitch")


    @commands.command()
    async def whistle(self, ctx):
        """Call Chomby"""

        await ctx.channel.connect()

    @whistle.before_invoke
    @chomby.before_invoke
    @snore.before_invoke
    @feed.before_invoke
    @dingdong.before_invoke
    @baddog.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Chomby can't find you (You need to be in a voice channel)")

    @commands.command()
    async def crate(self, ctx):
        """Put Chomby in their crate"""
        await ctx.voice_client.disconnect()


class Chomby(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or('..'), description="It's Chomby!", intents=intents)



@bot.event
async def on_ready():
    print('{0} is ready'.format(bot.user))


bot.add_cog(Dog(bot))

bot.run(os.getenv('TOKEN'))