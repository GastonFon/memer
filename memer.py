import discord
import json
import re

from os import environ

from MemeManager import MemeManager

#Creo el cliente de Discord
client = discord.Client()

#Constantes para las reacciones
LEFT_ARROW = "\U00002B05"
RIGHT_ARROW = "\U000027A1"

@client.event
async def on_ready():
    print("The bot is ready!")
    
@client.event
async def on_message(message):
    #Chequeamos que el bot no este respondiendo a otro bot
    if message.author.bot:
        return
    
    #Recibo el mensaje
    msg = str(message.content)
    channel = message.channel

    if not msg.startswith(';meme'):
        return

    msg = msg[6:]

    if msg.startswith("list"):
        try:
            page = int(msg[5:])
        except ValueError:
            page = 1
        finally:
            helpMsg = await channel.send(memeList(page))
            await helpMsg.add_reaction(LEFT_ARROW)
            await helpMsg.add_reaction(RIGHT_ARROW)
            return
    elif msg.startswith("help"):
        helpEmbed = getHelpEmbed()
        await message.channel.send(embed=helpEmbed)
        return

    if msg.startswith("general"):
        for i in message.guild.channels:
            if i.name == "memes" or i.name == "meme":
                channel = i
                break
        msg = msg[8:]

    if msg.startswith("anim"):
        isGif = True
        msg = msg[5:]
    else:
        isGif = False

    memeManager = MemeManager(msg)

    try:
        if not isGif:
            memeManager.getMeme()
            await channel.send(file=discord.File('temp.jpg'))
        else:
            memeManager.getAnimatedMeme()
            await channel.send(file=discord.File('temp.gif'))
        await message.delete()
    except ValueError:
        await message.channel.send("Joke not found.")
    except TypeError:
        await message.channel.send("Not enough arguments")
    except discord.errors.Forbidden:
        print("Tried to delete message")

@client.event
async def on_reaction_add(reaction, user):
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
    await message.edit(content=memeList(page))

def memeList(page):
    with open("metadata.json", "r") as metadata:
        data = json.load(metadata)

    lista = "```asciidoc"
    lista += "\nMemer, bot de discord\n"
    lista += "=====================\n"
    lista += "[Lista de memes: Página {}]\n".format(page)
    actual = 0
    for x in data:
        if actual // 10 != (page - 1):
            actual = actual + 1
            continue
        elif actual // 10 >= page:
            break
        actual = actual + 1
        maximo = 0
        for linea in data[x]['textpos']:
            maximo = max(maximo, linea['id'])
        if "anim" in data[x]:
            lista += ". {}: {} parametros\n".format(x, maximo+1)
        else:
            lista += "* {}: {} parámetros\n".format(x, maximo+1)
    lista += "Los memes que empiezan con . requieren usar anim\n"
    lista += "Los parámetros se separan con guión bajo (_)\n"
    lista += "Ejemplo: "
    lista += ";meme drake_memes con paint_memes con memer"
    lista += "```"
    return lista
   
def getHelpEmbed():
    with open("embed.json", "r") as embed:
        data = json.load(embed)
        helpEmbed = discord.Embed().from_dict(data)
    return helpEmbed

if __name__ == "__main__":
    client.run(environ['DISCORD_TOKEN'])
