'''This file pulls in all the cogs, sets up the bot and runs it'''

import logging
import discord
from discord.ext import commands
from settings import DEBUG, TOKEN

intents = discord.Intents.default()
intents.members = True

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# client = commands.Bot(command_prefix=commands.when_mentioned_or('!'),
#                       description="It's Dev Chomby!", intents=intents)

# client.remove_command('help')


# @client.command()
# async def help(ctx):
#     """displays command reference"""

#     embed = discord.Embed(color=discord.Color.orange(),
#                           description="test `test` \n `new` line")
#     embed.set_author(name='Help')
#     embed.add_field(name="help", value="Type `!help` to show this help")
#     embed.add_field(name='help', value="Returns this help text", inline=False)

#     await ctx.send(embed=embed)

# channel_id = []
# channel_name = []
# for server in bot.guilds:
#     for channel in server.channels:
#         if channel.name == 'chomby-test':
#             channel_id.append(channel.id)
#             channel_name.append(channel.name)
# await bot.get_channel(channel_id[0]).send('Ready in channel {}'.format(channel_name[0]))


class ChombyBot():
    '''initialize the bot'''

    def __init__(self):
        self.client = commands.Bot(command_prefix='!')
        self._on_ready = self.client.event(self.on_ready)
        self._on_message = self.client.event(self.on_message)
        self._on_disconnect = self.client.event(self.on_disconnect)
        self._on_error = self.client.event(self.on_error)

    async def on_ready(self):
        """bot ready event"""
        await self.client.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening, name="!help"))

        logger.info('{0} is ready'.format(self.client.user))
        logger.info('----')
        print('Bot is ready')
        if DEBUG:
            logger.info('Bot is in debug mode')

    async def on_message(self, message):
        """Listens for user messages """
        if message.author == self.client.user:
            return
        if message.content.lower() == "good boy" or message.content.lower() == 'good dog':
            await message.add_reaction('brenda:800427845620072488')
            await message.channel.send('<:brenda:800427845620072488>')
        await self.client.process_commands(message)
    
    async def on_disconnect(self):
        '''Logs disconnect messages'''

        logger.info('Bot has disconnected')
    
    async def on_error(self, event, *args, **kwargs):
        '''Logs errors to log file'''

        logger.info('ERROR: {}'.format(event))

    def run(self):
        '''run the bot'''

        self.client.load_extension('cogs.dev')
        self.client.load_extension('cogs.pet')
        self.client.load_extension('cogs.misc')
        self.client.load_extension('cogs.music')

        self.client.run(TOKEN)


if __name__ == "__main__":
    run_bot = ChombyBot()
    run_bot.run()
