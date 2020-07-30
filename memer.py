import discord
import json
import os 
import re

from MemeManager import MemeManager

#Make the discord client
client = discord.Client()

@client.event
async def on_ready():
    print("The bot is ready!")
    
@client.event
async def on_message(message):
    #Chequeamos que el bot no se esté respondiendo solo
    if message.author == client.user:
        return
    
    #Recibo el mensaje
    msg = str(message.content)

    if not msg.startswith(';meme'):
        return

    msg = msg[6:]

    if msg.startswith("list") or msg.startswith("help"):
        try:
            page = int(msg[5:])
        except ValueError:
            page = 1
        finally:
            helpMsg = await message.channel.send(help(page))
            await helpMsg.add_reaction("\U00002B05")
            await helpMsg.add_reaction("\U000027A1")
            return
        
    memeManager = MemeManager(msg)
    
    try:
        memeManager.getMeme()
        await message.channel.send(file=discord.File('temp.jpg'))
    except ValueError:
        await message.channel.send("Joke not found.")

    try:
        await message.delete()
    except discord.errors.Forbidden:
        print("Tried to delete message")

@client.event
async def on_reaction_add(reaction, user):
    LEFT_ARROW = "\U00002B05"
    RIGHT_ARROW = "\U000027A1"
    message = reaction.message
    msg = str(message.content)
    if user == client.user:
        return
    if message.author != client.user:
        return
    emoji = str(reaction)
    if emoji != LEFT_ARROW and emoji != RIGHT_ARROW:
        return
    pageRegex = re.compile(r"\d+\]")
    page = int(pageRegex.search(msg).group(0)[:-1])
    if emoji == LEFT_ARROW:
        page = max(page - 1, 1)
    elif emoji == RIGHT_ARROW:
        page = page + 1
    await message.edit(content=help(page))

    

def help(page):
    with open("metadata.json", "r") as metadata:
        data = json.load(metadata)
    ayuda = "```asciidoc"
    ayuda += "\nMemer, bot de discord\n"
    ayuda += "=====================\n"
    ayuda += "[Lista de memes: Página {}]\n".format(page)
    actual = 0
    for x in data:
        if actual // 10 != (page - 1):
            actual = actual + 10
            continue
        actual = actual + 1
        maximo = 0
        for linea in data[x]['textpos']:
            maximo = max(maximo, linea['id'])
        ayuda += "* {}: {} parámetros\n".format(x, maximo+1)
    ayuda += "Los parámetros se separan con guión bajo (_)\n"
    ayuda += "Ejemplo: "
    ayuda += ";meme drake_memes con paint_memes con memer"
    ayuda += "```"
    return ayuda
    
client.run(os.environ['DISCORD_TOKEN'])
