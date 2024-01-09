import sqlite3

con = sqlite3.connect("bandmaker.db")
cur = con.cursor()
stock = "lol"
cur.execute('''DELETE FROM stocks WHERE stockID = (?)''', (stock,))

def showStocks():
    stockList = ""
    for row in cur.execute("SELECT stockID FROM stocks"):
        stockList += row[0] + " "
    return stockList

print(showStocks())
con.close