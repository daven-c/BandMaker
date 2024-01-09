import discord
import sqlite3
from discord.ext import commands

discord_token = "MTE5MjkyODY0OTgwNTA0NTk0Mw.GwEF8F.MccvgaldNMJxes3Qi9fHcxaukFLO5SL0Hg9XG4"
intents = discord.Intents.all()
client = commands.Bot(command_prefix='/', intents=intents)

#initialize database connection
con = sqlite3.connect("bandmaker.db") 
cur = con.cursor() 

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    cur.execute('''
    CREATE TABLE IF NOT EXISTS stocks(
        stockID text,
        support text,
        resistance text
        )
    ''')
    con.commit() #use commit to save changes

@client.command(name="trackStock", help="Adds stock to the watchlist")
async def add_stock(ctx, stock):
    cur.execute('''
        INSERT INTO stocks (stockID, support, resistance)
            VALUES (?,?,?)
    ''', [str(stock),'0','0']) #use second parameter to input python variables, must be in tuple form
    con.commit()
    await ctx.send("I am now tracking " + stock)

@client.command(name="showList", help="Show the stocks currently on the watchlist")
async def show_list(ctx):
    stockList = ""
    for row in cur.execute("SELECT stockID FROM stocks"):
        stockList += row[0] + " "
    if stockList == "":
        await ctx.send("You have no stocks on the watch list")
    else:
        await ctx.send(stockList)

@client.command(name="removeStock", help="Removes the given stock from the watchlist")
async def remove_stock(ctx, stock):
    cur.execute('''DELETE FROM stocks WHERE stockID = (?)''', (stock,))
    con.commit()
    await ctx.send(stock + " has been removed from the watch list")

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


