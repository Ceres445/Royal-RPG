from discord.ext import commands
import traceback
import discord

from discord.ext.commands.errors import *
import json
from discord.ext.commands import check_any
from .utils.func import read
from .utils.embedmanager import start, profile
from discord.ext.commands.errors import BadArgument


class game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='shop')
    async def shop(self, ctx):
        await ctx.send('aye shop')

    @commands.command(name='bal')
    async def bal(self, ctx):
        await ctx.send('you bal is 0')

    @commands.command(name='start')
    async def start(self, ctx):
        def in_channel(message):
            if message.channel.id == ctx.channel.id and message.author == ctx.author:
                return True
            else:
                return False
        info = await self.bot.db.fetch("SELECT * FROM user_data where id = $1", ctx.author.id)
        print(info)
        if info:
            await ctx.send("you have already completed character creation")
        else:
            with open(file='start.json', mode='r') as f:
                data = json.load(f)
            loadout = []
            for key, value in data.items():
                await ctx.send(embed=start(key, value))
                message = await self.bot.wait_for('message', timeout=30.0, check=in_channel)
                try:
                    int(message.content)
                except:
                    raise BadArgument
                    return
                if int(message.content) > len(value):
                    raise BadArgument
                else:
                    chosen = int(message.content) - 1
                    loadout.append(chosen)
                    await ctx.send(f"you have chosen {chosen}")
            print(loadout)
            await self.bot.db.execute("INSERT INTO user_data (id, loadout) VALUES ($1, $2)", ctx.author.id, loadout)
            await ctx.send("your creation is complete")

    @start.error
    async def error(self, ctx, error):
        if isinstance(error, BadArgument):
            await ctx.send("please enter the number beside your choice, not the choice or any other number")

    @commands.command(name='profile')
    async def profile(self, ctx):
        info = await self.bot.db.fetchrow("select * from user_data where id = $1", id)
        if not info:
            await ctx.send("you have not completed your character creation, use `+start` to create your character")
        else:
            with open(file='start.json', mode='r') as f:
                data = json.load(f)
            for key, value in data.items:
                data[key][info]
            key = list(data.keys())



def setup(bot):
    bot.add_cog(game(bot))
