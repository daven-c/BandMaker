import discord
from datetime import datetime
from discord import app_commands
from discord.ext import commands
import sqlite3
import asyncio
from typing import Optional, List, Tuple, Dict
import yfinance as yf
import os


# BOT Settings
TOKEN = "MTE5MjkyODY0OTgwNTA0NTk0Mw.GwEF8F.MccvgaldNMJxes3Qi9fHcxaukFLO5SL0Hg9XG4"
LOGS = True
LOGS_CHANNEL_ID = 1194393666740048015
PRIV_METHODS = ['test']

# BOT Intialization
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Database connection
con = sqlite3.connect("bandmaker.db")
cur = con.cursor()


async def sendLogs(content: str, command_name: str = None):
    if LOGS:
        log_channel = client.get_channel(LOGS_CHANNEL_ID)
        now = datetime.now()
        current_time = now.strftime('%H:%M')
        if command_name is not None:
            output = f'{command_name} - {current_time}\n{content}'
        else:
            output = f'{content} - {current_time}'
        print(output)
        await log_channel.send(f"```{output}```")


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
    con.commit()  # use commit to save changes
    await tree.sync()
    await alert_user()
    # await sendLogs('client ready')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'for help'))


@tree.command(name='help', description='help list')
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title=f'Bot Commands', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                          colour=discord.Colour.red())
    embed.add_field(name='General', inline=False,
                    value='**/online**: check if client is online')
    commands_str = '\n'.join(
        [f'**/{cmd.name}**: {cmd.description}' for cmd in tree.get_commands() if cmd.name not in PRIV_METHODS])
    embed.add_field(name='Bot', inline=False, value=commands_str)
    await interaction.response.send_message(embed=embed)


@tree.command(name='online', description='check if bot is responsive')
async def check_online(interaction: discord.Interaction):
    await interaction.response.send_message(content='\N{CHECK MARK}')


@tree.command(name='echo', description='<msg> | ghost echo a message')
async def echo(interaction: discord.Interaction, msg: str):
    await interaction.response.send_message('...', delete_after=.01)
    await interaction.channel.send(msg)


@tree.command(name="track-stock", description="Adds stock to the watchlist")
async def add_stock(interaction: discord.Interaction, stock: str):
    cur.execute('''
        INSERT INTO stocks (stockID, support, resistance)
            VALUES (?,?,?)
    ''', [str(stock), '0', '0'])  # use second parameter to input python variables, must be in tuple form
    con.commit()
    await interaction.response.send_message("I am now tracking " + stock)


@tree.command(name="show-stocks", description="Show the stocks currently on the watchlist")
async def show_list(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f'{interaction.user.name}', colour=discord.Colour.red())

    stockList = []
    for row in cur.execute("SELECT stockID FROM stocks"):
        stockList.append(row[0])
    embed.add_field(name='Watch List', inline=False,
                    value='\n'.join(stockList))

    await interaction.response.send_message(embed=embed)


@tree.command(name="remove-stock", description="Removes the given stock from the watchlist")
async def remove_stock(interaction: discord.Interaction, stock: str):
    cur.execute('''DELETE FROM stocks WHERE stockID = (?)''', (stock,))
    con.commit()
    await interaction.response.send_message(stock + " has been removed from the watch list")


@tree.command(name='stock-info', description='Show information about a stock')
async def stock_info(interaction: discord.Interaction, stock: str):
    embed = discord.Embed(title=f'{stock}', colour=discord.Colour.red())

    embed.add_field(name='temp', value='body')

    info = yf.Ticker(stock)
    data = info.history(period='1y', interval='1d')
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'],
                    close=data['Close'], high=data['High'], low=data['Low'])])
    fig.write_image(f"graphs/{interaction.user.name}-{stock}.png")
    file = discord.File(
        f"graphs/{interaction.user.name}-{stock}.png", filename="image.png")
    embed.set_image(url="attachment://image.png")

    embed.add_field(name='temp', value='body')

    await interaction.response.send_message(embed=embed, file=file)
    os.remove(f"graphs/{interaction.user.name}-{stock}.png")


async def alert_user():
    while True:
        # implement stock pattern recognition
        embed = discord.Embed(title=f'Pattern Detected',
                              colour=discord.Colour.red())
        embed.add_field(name='STOCK_NAME', inline=False, value='pattern name')
        embed.add_field(name='BEARISH/BULLISH', value='CONFIDENCE_PERCENTAGE')
        await asyncio.sleep(10)
        channel = client.get_channel(1194389374532603914)
        await channel.send(embed=embed)


client.run(TOKEN)
