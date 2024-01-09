import discord
from discord.ext import commands


discord_token = "MTE5MjkyODY0OTgwNTA0NTk0Mw.GwEF8F.MccvgaldNMJxes3Qi9fHcxaukFLO5SL0Hg9XG4"
intents = discord.Intents.all()
client = commands.Bot(command_prefix='/', intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.listen()
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content.lower()

    if msg == 'gnaij':
        # await message.channel.send(' is fat')
        await message.channel.send("https://media.discordapp.net/attachments/801962896761946132/1095392190424956959/aaaah.png?width=1338&height=1014")
        await message.channel.send("https://tenor.com/view/sheesh-papa-kermit-drive-gif-12861924")


    if msg == 'alan':
        await message.channel.send(' is fat')

    # if 'e' in msg:
    #     await message.channel.send("SUB TO HUSHVALO")

    if msg == 'i love bandmaker':
        await message.channel.send('I love you too {}'.format(message.author.name))


client.run(discord_token)


