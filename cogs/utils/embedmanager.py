import discord

def start(key, value):
    description = f"Choose your {key}\n "
    j = 1
    for i in value:
        description = description + f"{j}. {i}\n"
        j+= 1
    embed = discord.Embed(title='CHARACTER CREATION', description=description, color=3837)
    return embed

def profile(key, list):
    description= str()
    for i , j in key, list:
        description += f"{i}: {j} \n"
    embed = discord.Embed(title='Character Profile', description=description, color=3837)
    return embed
