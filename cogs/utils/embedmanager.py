import discord

def start(key, value):
    description = f"Choose your {key}\n "
    j = 1
    for i in value:
        description = description + f"{j}. {i}\n"
        j+= 1
    embed = discord.Embed(title='CHARACTER CREATION', description=description, color=3837)
    return embed

def profile(name, key, list):
    description= f"Name: {name} \n"
    for i in range(5):
        description += f"{key[i]}: {list[i]} \n"
    embed = discord.Embed(title='Character Profile', description=description, color=3837)
    return embed
