from discord.ext import commands
import discord

import json


from aiohttp import ClientSession
import datetime
import asyncio
from cogs.utils.database import DataBase
initial_cogs = [
    'cogs.currency'
]


class Helper(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=kwargs.pop('command_prefix', ['+']), case_insensitive=True, **kwargs)
        self.session = ClientSession(loop=self.loop)
        self.start_time = datetime.datetime.utcnow()
        self.clean_text = commands.clean_content(escape_markdown=True, fix_channel_mentions=True)
        self.db = None

    """"  Events  """

    async def on_ready(self):
        print(f'Successfully logged in as {self.user}\nSharded to {len(self.guilds)} guilds')
        await self.change_presence(status=discord.Status.online, activity=discord.Game(name='use the prefix "+"'))
        for ext in initial_cogs:
            self.load_extension(ext)

    async def on_connect(self):
        self.db = await DataBase.create_pool(bot=self, uri="postgresql://localhost/royal", loop=self.loop)

    @classmethod
    async def setup(cls, **kwargs):
        bot = cls()
        try:
            with open('cogs/json/token.json', 'r') as f:
                token = json.load(f)
            await bot.start(token['token'], **kwargs)

        except KeyboardInterrupt:
            await bot.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Helper.setup())
