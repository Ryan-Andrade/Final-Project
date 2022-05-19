# Dependencies
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt

# A function to download data from Yahoo Finance and manipulate it
def downloadStockData(tickers: list[str]):
    for ticker in tickers:
        data = yf.download(ticker, '2021-01-01', dt.datetime.date(dt.datetime.now()).isoformat(), interval='1d')
        data.drop(['Adj Close', 'Volume'], axis=1, inplace=True)
        data['Day Result'] = np.where(data['Close'] > data['Open'], 1, 0)
        data.to_csv(f'Data/{ticker}.csv')