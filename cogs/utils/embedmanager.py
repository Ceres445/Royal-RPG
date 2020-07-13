import discord


def start(key, value):
    description = f"Choose your {key}\n "
    j = 1
    for i in value:
        description = description + f"{j}. {i}\n"
        j += 1
    embed = discord.Embed(title='CHARACTER CREATION', description=description, color=3837)
    return embed


def profile(name, key, list1):
    description = f"Name: {name} \n"
    for i in range(5):
        description += f"{key[i]}: {list1[i]} \n"
    embed = discord.Embed(title='Character Profile', description=description, color=3837)
    return embed


def inv(weapon):
    description = f"Broken {weapon[0]} \nMalfunctioning {weapon[1]}"
    embed = discord.Embed(title='Inventory', description=description, color=3837)
    return embed

def shop(title, list1: dict):
    description = str()
    for i in list1:
        item = list1[i]
        description+= f"**{i}** : {item[1]}\n Cost: {item[0]} \n ```{item[2]}``` \n"
    return discord.Embed(title= title, description= description, color= 3837)
