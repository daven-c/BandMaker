import discord
from datetime import datetime
from discord import app_commands
from discord.ext import commands
import sqlite3
import asyncio
from typing import Optional, List, Tuple, Dict
import yfinance as yf
from patterns.patterns import *


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
    
    interval_set = {"1m","2m","5m","15m","30m","60m"}
    interval_set.add(interval.lower()) 
    print(interval)
    if len(interval_set) != 6:#check if the interval is in the set above
        await interaction.response.send_message("Error: The interval you entered is not valid\nValid intervals: 1m,2m,5m,15m,30m,60m")
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
    for row in cur.execute("SELECT * FROM stocks"):
        stockList.append(str(row[0]) + " " + str(row[1]))
    embed.add_field(name='Watch List(Ticker, Interval)', inline=False,
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

# TODO: change to get most recent candles
async def alert_user():
    #1m,2m,5m,15m,30m,60m
    channel = client.get_channel(1194389374532603914)
    pattern_matchers = [MomentumCandle(), EngulfingCandle(), MultipleCandle(), DojiCandle(), ShootingStar(), Tweezer(), Marubozu()]
    time = 0
    while True:             
        time += 1
        if time == 60: # Reset the clock every hour for the interval checking
            time = 0

        await channel.send("Checking all stocks..... time elapsed: " + str(time))#testing

        tickers = []
        for row in cur.execute('SELECT * FROM stocks'): # Collect all tickers and time intervals that need to be checked
            interval = row[1]
            if interval == '1m':
                tickers.append((row[0], row[1]))
                print(row[0] + " " + row[1])
            elif interval == '2m' and time % 2 == 0:
                tickers.append((row[0], row[1]))
                print(row[0] + " " + row[1])
            elif interval == '5m' and time % 5 == 0:
                tickers.append((row[0], row[1]))
                print(row[0] + " " + row[1])
            elif interval == '15m' and time % 15 == 0:
                tickers.append((row[0], row[1]))
                print(row[0] + " " + row[1])
            elif interval == '30m' and time % 30 == 0:
                tickers.append((row[0], row[1]))
                print(row[0] + " " + row[1])
            elif interval =='60' and time == 0:
                tickers.append((row[0], row[1]))
                print(row[0] + " " + row[1])

        for i in range(len(tickers)):
            info = yf.Ticker(tickers[i][0])
            data = info.history(period='1d', interval=tickers[i][1]) #Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            for j in range(len(pattern_matchers)):
                patterns = pattern_matchers[j].process(data.tail(pattern_matchers[j].CANDLES_REQUIRED))
                if len(patterns) == 0:
                    continue
                detection = patterns[-1]
                embed = discord.Embed(title=f'Pattern Detected',
                                        colour=discord.Colour.red())
                embed.add_field(name=tickers[i][0], inline=False, value=pattern_matchers[j].NAME)
                embed.add_field(name='Direction: ', value='BULLISH' if detection[-1] == 1 else 'BEARISH')
                await channel.send(embed=embed)
        
        await asyncio.sleep(60)#check/refresh every one minute

client.run(TOKEN)
