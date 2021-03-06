from discord.ext import commands
import json

from .utils.embedmanager import start, profile, inv, shop
from discord.ext.commands.errors import BadArgument
from asyncio import TimeoutError


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(file="cogs/json/start.json", mode='r') as f:
            starter = json.load(f)
        with open("cogs/json/items.json", "r") as f:
            items = json.load(f)
        self.items = items
        self.starter = starter

    @commands.command(name='shop', aliases=['store'])
    async def shop(self, ctx, n: int = None):
        """Shows the items you can buy"""
        if n is None:
            n = 1
        key = list(self.items.keys())[n - 1]
        await ctx.send(embed=shop(key, self.items[key]))

    @commands.command(name='bal', aliases=['balance'])
    async def bal(self, ctx):
        """Shows your balance"""
        data = await self.bot.db.fetchrow("SELECT * FROM user_data WHERE id = $1", ctx.author.id)
        if not data:
            await ctx.send("you have not completed your character creation, use `+start` to create your character")
        else:
            await ctx.send(f"your balance is : {data['money']}")

    @commands.command(name='start')
    async def start(self, ctx):
        """starts your game by creating your character"""

        def in_channel(ok):
            if ok.channel.id == ctx.channel.id and ok.author == ctx.author:
                return True
            else:
                return False

        info = await self.bot.db.fetch("SELECT * FROM user_data where id = $1", ctx.author.id)
        if info:
            await ctx.send("you have already completed character creation")
        else:
            data = self.starter
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
                    await ctx.send(f"you have chosen {chosen + 1}. {data[key][chosen]}")
            await self.bot.db.execute("INSERT INTO user_data (id, loadout, money) VALUES ($1, $2, 1000)",
                                      ctx.author.id, loadout)
            await ctx.send("your creation is complete")

    @start.error
    async def error(self, ctx, error):
        if isinstance(error, BadArgument):
            await ctx.send("please enter the number beside your choice, not the choice or any other number")

    @commands.command(name='profile')
    async def profile(self, ctx):
        """Shows your profile"""
        info = await self.bot.db.fetchrow("select * from user_data where id = $1", ctx.author.id)
        if not info:
            await ctx.send("you have not completed your character creation, use `+start` to create your character")
        else:
            data = self.starter
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
        """resets all your character data"""

        def check(reaction, user):
            return user == ctx.message.author

        info = await self.bot.db.fetchrow("select * from user_data where id = $1", ctx.author.id)
        if not info:
            await ctx.send("you don't have a character created")
        else:
            message = await ctx.send("Are you sure?")
            await message.add_reaction("\U0001f44d")
            await message.add_reaction("\U0001f44e")
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == "\U0001f44d":
                await self.bot.db.execute("DELETE from user_data where id = $1", ctx.author.id)
                await ctx.send("Your character has been deleted")
            else:
                await ctx.send("phew dodged a bullet")

    @commands.command(name='inv', aliases=["inventory"])
    async def inv(self, ctx):
        """Shows your items"""
        info = await self.bot.db.fetchrow("select * from user_data where id = $1", ctx.author.id)
        weapons = [self.starter["Primary Weapon"][info['loadout'][0]],
                   self.starter["Secondary Weapon"][info['loadout'][1]]]
        await ctx.send(embed=inv(weapons))

    @commands.command()
    async def buy(self, ctx, arg: int = None):
        #make here and remove comment
        if arg is None:
            await ctx.send('what u want to buy')




def setup(bot):
    bot.add_cog(Game(bot))
