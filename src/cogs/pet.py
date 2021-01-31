'''Handles pet related functions for ChombyBot'''

import asyncio
import discord
from discord.ext import commands


class Pet(commands.Cog):
    ''' Pet commands class '''

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def find(self, ctx):
        ''' Find users using voice '''
        users = ctx.guild.voice_channels

        #userlist = []
        for user in users:
            for member in user.members:
                print(member.name)

    @commands.command()
    async def sic(self, ctx, member: discord.Member):
        """ @ a user to sic Chomby on them"""

        try:
            voice_channel = member.voice.channel

            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(voice_channel)
            await voice_channel.connect()
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio('chomby_audio/sic.mp3'))
            ctx.voice_client.play(source)

            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)

            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
        except AttributeError:
            await ctx.send("User must be in a voice channel")

    @commands.command(help="Call Chomby over")
    async def chomby(self, ctx):
        '''Call Chomby over'''
        query = 'chomby_audio/bark2.wav'
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)

        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(help="Give Chomby a snack")
    async def feed(self, ctx):
        ''' feed chomby '''

        query = 'chomby_audio/feeding.mp3'
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)

        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(help="Give Chomby a snack")
    async def snore(self, ctx, *, query='chomby_audio/snore.mp3'):
        ''' listen to Chomby sleep '''

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)

        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(help="Someone just rang the doorbell..")
    async def dingdong(self, ctx, *, query='chomby_audio/dingdong.mp3'):
        ''' Someone just rang the doorbell... '''
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
        '''Check if user is connected to a voice channel before running '''
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Chomby can't find you (You need to be in a voice channel)")

    @chomby.after_invoke
    async def done_voice(self, ctx):
        print('done')

    @commands.command()
    async def crate(self, ctx):
        """Put Chomby in their crate"""
        await ctx.voice_client.disconnect()


def setup(client):
    ''' Setup pet cog '''
    client.add_cog(Pet(client))
