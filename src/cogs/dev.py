'''Dev commands for ChombyBot'''

from discord.ext import commands


class Dev(commands.Cog):
    """ A dev cog"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        """sends pong"""
        await ctx.send("pong")


def setup(client):
    '''setup cog'''
    client.add_cog(Dev(client))
