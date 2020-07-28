import discord
import json
import os 

#Import PIL to edit images
from PIL import Image, ImageDraw, ImageFont

#Make the discord client
client = discord.Client()

@client.event
async def on_ready():
    print("The bot is ready!")

def getParams(msg):
    #Devuelve una lista con valores, separados por '_'
    #Primero nombre del meme, y luego los textos del mismo
    return msg.split('_')

#Get meme
def getMeme(memeInfo): 
    try: 
        texto = getParams(memeInfo)

        image = Image.open('./img/'+texto[0].lower()+'.jpg')
        aspectRatio = image.size[1] / image.size[0]
        image = image.resize((512, round(aspectRatio * 512)))
        font_type = ImageFont.truetype('./fonts/Roboto.ttf', 32)
        draw = ImageDraw.Draw(image)
       
        with open("metadata.json", "r") as data:
            currentMeme = str(texto[0].lower())
            texto = texto[1:]
            memes = json.load(data)
            textPos = memes[currentMeme]['textpos']
            if "color" in memes[currentMeme]:
                color = tuple(memes[currentMeme]['color'])
            else:
                color = (0, 0, 0) #color negro por default
            for i in range(len(textPos)):
                pos = (textPos[i]['x'], textPos[i]['y'])
                linea = texto[textPos[i]['id']]
                #dibuja el texto en el meme dependiendo de lo que dice metadata.json
                draw.text(xy=pos, text=linea, fill=color, font=font_type)
        
        image.save('./tmp/meme.jpg')
        return './tmp/meme.jpg'
    except:
        return ''
    
def help():
    data = json.load(open("metadata.json", "r"))
    ayuda = "```asciidoc"
    ayuda += "\nMemer, bot de discord\n"
    ayuda += "=====================\n"
    ayuda += "[Lista de memes]\n"
    for x in data:
        maximo = 0
        for linea in data[x]['textpos']:
            maximo = max(maximo, linea['id'])
        ayuda += "* {}: {} parámetros\n".format(x, maximo+1)
    ayuda += "Los parámetros se separan con guión bajo (_)\n"
    ayuda += "Ejemplo: ;meme drake_memes con paint_memes con memer"
    ayuda += "```"
    return ayuda
    
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
        if msg == "list" or msg == "help":
            await message.channel.send(help())
            return
        img = getMeme(msg)

        if len(str(img)) > 0:
            await message.channel.send(file=discord.File(img))
            await message.delete()
        else:
            await message.channel.send("Joke not found.")

client.run(os.environ['DISCORD_TOKEN'])
