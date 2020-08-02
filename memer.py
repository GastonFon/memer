import discord
import json
import re

from discord.ext import commands
from os import environ

from MemeManager import MemeManager

client = commands.Bot(
    command_prefix = ";meme ",
    case_insensitive = False,
    owner_ids = (
        550695764041400351, 
        639924381690101771, 
        208621559709958145
    ),
    help_command = None,
    self_bot = False
)

memeManager = MemeManager()

SPECIAL_ARGS = ('anim', 'general')

EMOJIS = ("\U00002B05", "\U000027A1")

@client.event
async def on_ready():
    print("The bot is ready!")

@client.command()
async def list(ctx, page=1):
    memeList = MemeManager.getMemeList(page)
    listMessage = await ctx.send(memeList)
    await listMessage.add_reaction(EMOJIS[0])
    await listMessage.add_reaction(EMOJIS[1])

@client.command()
async def help(ctx):
    with open("embed.json", "r") as embed:
        data = json.load(embed)
        helpEmbed = discord.Embed().from_dict(data)
    await ctx.send(embed=helpEmbed)

@client.command()
async def get(ctx, *args):
    if "anim" in args:
        isGif = True
    else:
        isGif = False

    channel = ctx.message.channel
    if "general" in args:
        if not(channel.type.private or channel.type.group):
            for i in ctx.message.guild.channels:
                if i.name == "memes":
                    channel = i
                break

    filteredArgs = [item for item in args if item not in SPECIAL_ARGS]
    
    memeManager.setText(filteredArgs)

    try:
        if isGif:
            memeManager.getAnimatedMeme()
            imageName = "temp.gif"
        else:
            memeManager.getMeme()
            imageName = "temp.jpg"
    except ValueError:
        await channel.send("Joke not found")
        return
    except TypeError:
        await channel.send("Not enough arguments")
        return

    try:
        await channel.send(file=discord.File(imageName))
        await ctx.message.delete()
    except discord.errors.Forbidden:
        print("Tried to delete message")

@client.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    msg = str(message.content)

    if user.bot or message.author != client.user:
        return

    emoji = str(reaction)

    if emoji not in EMOJIS:
        return

    pageRegex = re.compile(r"\d+\]")
    page = int(pageRegex.search(msg).group(0)[:-1])

    if emoji == EMOJIS[0]:
        page = max(page - 1, 1)
    elif emoji == EMOJIS[1]:
        page = page + 1

    memeList = MemeManager.getMemeList(page)
    await message.edit(content=memeList)

if __name__ == "__main__":
    client.run(environ["DISCORD_TOKEN"])
