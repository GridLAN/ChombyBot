import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def test(self, ctx):
        """A test command"""
        await ctx.send('test')
    
    @test.group()
    async def subtest(self, ctx):
        await ctx.send('subcommand of test')


def setup(bot):
    bot.add_cog(Misc(bot))