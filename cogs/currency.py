from discord.ext import commands
import json

from .utils.embedmanager import start, profile
from discord.ext.commands.errors import BadArgument
from asyncio import TimeoutError

class Game(commands.Cog):
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
        def in_channel(ok):
            if ok.channel.id == ctx.channel.id and ok.author == ctx.author:
                return True
            else:
                return False
        info = await self.bot.db.fetch("SELECT * FROM user_data where id = $1", ctx.author.id)
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
                except TimeoutError:
                    raise BadArgument
                if int(message.content) > len(value):
                    raise BadArgument
                else:
                    chosen = int(message.content) - 1
                    loadout.append(chosen)
                    await ctx.send(f"you have chosen {chosen+ 1}. {data[key][chosen]}")
            print(loadout)
            await self.bot.db.execute("INSERT INTO user_data (id, loadout) VALUES ($1, $2)", ctx.author.id, loadout)
            await ctx.send("your creation is complete")

    @start.error
    async def error(self, ctx, error):
        if isinstance(error, BadArgument):
            await ctx.send("please enter the number beside your choice, not the choice or any other number")

    @commands.command(name='profile')
    async def profile(self, ctx):
        info = await self.bot.db.fetchrow("select * from user_data where id = $1", ctx.author.id)
        if not info:
            await ctx.send("you have not completed your character creation, use `+start` to create your character")
        else:
            with open(file='start.json', mode='r') as f:
                data = json.load(f)
            key = list(data.keys())
            loadout = list()
            for i in range(5):
                index = info['loadout'][i]
                loadout.append(data[key[i]][index])
                if key[i] == "Team":
                    key[i] = "Allegiance"
            await ctx.send(embed=profile(ctx.author.name, key, loadout))

    @commands.command(name='reset')
    async def reset(self, ctx):
        def in_channel(ok):
            if ok.channel.id == ctx.channel.id and ok.author == ctx.author:
                return True
            else:
                return False
        info = await self.bot.db.fetchrow("select * from user_data where id = $1", ctx.author.id)
        if not info:
            await ctx.send("you don't have a character created")
        else:
            await ctx.send("are you sure (yes/no) if you dont reply it will be cancelled")
            message = await self.bot.wait_for('message', timeout=30.0, check=in_channel)
            if message.content.lower == 'yes':
                await self.bot.db.execute("DELETE from user_data where id = $1", ctx.author.id)
                await ctx.send("i have deleted your character")
            else:
                await ctx.send("phew dodged a bullet")


def setup(bot):
    bot.add_cog(Game(bot))
