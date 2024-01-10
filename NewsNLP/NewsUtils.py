import yfinance as yf
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import requests as req
from bs4 import BeautifulSoup
import re

# Requests args
HEADERS = {'User-Agent': 'Chrome/120.0.6099.216'}
CHUNK_SIZE = 1024

def fetch_articles(symbol: str) -> tuple[int, list[str]]:
    """
    Summary:
        Fetches and returns recent articles associated with a ticker

    Args:
        symbol (str): Ticker symbol of the stock

    Returns:
        tuple[int, list[str]]: Returns the number of articles sourced and a list containing the content of the articles
    """
    
    articles = []
    successes = 0

    info = yf.Ticker(symbol)

    for src in info.news:
        resp = req.get(src['link'], allow_redirects=True, headers=HEADERS, stream=True)

        if resp.status_code == 200:
            successes += 1

            content = "".join([batch for batch in resp.iter_content(chunk_size=CHUNK_SIZE, decode_unicode=True)])
                
            soup = BeautifulSoup(content, 'html.parser')
            tags = soup.find_all('div', class_='caas-body')[0].find_all('p')
            cleaned_content = re.sub(r'<.*?>|[\[\]]', '', str(tags)).replace('.,', '.')
            
            articles.append(cleaned_content)

    return successes, articles