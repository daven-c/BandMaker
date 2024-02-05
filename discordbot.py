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
TOKEN = open('secrets', 'r').readline().strip()
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
        stockID text UNIQUE,
        interval text
        )
    ''')
    con.commit()  # use commit to save changes
    await tree.sync()
    #await alert_user()
    #await sendLogs('client ready')
    await alert_user()
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

@tree.command(name="track-stock", description="Adds stock to the watchlist\nstock: name of ticker\ninterval: How often candlesticks should be analyzed")
async def add_stock(interaction: discord.Interaction, stock: str, interval: str):
    stock_data = yf.Ticker(str(stock))
    info = stock_data.info#get info to see if the ticker is valid
    if len(info) == 1: #tell user that the stock name is not valid
        await interaction.response.send_message("Error: The stock name you entered is not valid: " + stock)
        return
    
    interval_set = {"1m","2m","5m","15m","30m","60m","90m","1h","1d","5d","1wk","1mo","3mo"}
    interval_set.add(interval.lower()) 
    if len(interval_set) != 13:#check if the interval is in the set above
        await interaction.response.send_message("Error: The interval you entered is not valid\nValid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo")
        return 
    
    try:#check if we are already tracking the stock 
        stock = stock.upper()#make all stock names uppercase only
        cur.execute('''
            INSERT INTO stocks (stockID, interval)
                VALUES (?,?)
        ''', [str(stock), str(interval)]) #use second parameter to input python variables, must be in tuple form
        con.commit()
        await interaction.response.send_message("I am now tracking " + stock + " with " + interval + " interval")
    except Exception as e:
        await interaction.response.send_message("Error: You are already tracking " + stock)
  
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
    try:
        stock = stock.upper()
        cur.execute('''DELETE FROM stocks WHERE stockID = (?)''', (stock,))
        con.commit()
        await interaction.response.send_message(stock + " has been removed from the watch list")
    except Exception as e:
        await interaction.response.send_message("Error" + stock + " is not on the watch list")

async def alert_user():
    while True:
        # implement stock pattern recognition
        embed = discord.Embed(title=f'Pattern Detected',
                              colour=discord.Colour.red())
        embed.add_field(name='STOCK_NAME', inline=False, value='pattern name')
        embed.add_field(name='BEARISH/BULLISH', value='CONFIDENCE_PERCENTAGE')
        await asyncio.sleep(60)
        channel = client.get_channel(1194389374532603914)
        await channel.send(embed=embed)


client.run(TOKEN)
