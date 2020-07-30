import discord
import json
import os 

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

    if not msg.startswith(';'):
        return

    msg = msg[1:]

    if msg.startswith('meme'):
        msg = msg[5:]
        if msg.startswith("list") or msg.startswith("help"):
            try:
                page = int(msg[5:])
            except ValueError:
                page = 1
            finally:
                await message.channel.send(help(page))
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

def help(page):
    with open("metadata.json", "r") as metadata:
        data = json.load(metadata)
    ayuda = "```asciidoc"
    ayuda += "\nMemer, bot de discord\n"
    ayuda += "=====================\n"
    ayuda += "[Lista de memes: Página {}]\n".format(page)
    actual = 0
    for x in data:
        actual = actual + 1
        if actual // 10 != (page - 1):
            continue
        maximo = 0
        for linea in data[x]['textpos']:
            maximo = max(maximo, linea['id'])
        ayuda += "* {}: {} parámetros\n".format(x, maximo+1)
    ayuda += "Los parámetros se separan con guión bajo (_)\n"
    ayuda += "Ejemplo: ;meme drake_memes con paint_memes con memer"
    ayuda += "```"
    return ayuda
    
client.run(os.environ['DISCORD_TOKEN'])
