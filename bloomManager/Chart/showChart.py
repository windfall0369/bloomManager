import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 1d 차트
def day_chart(ticker, start, end):
    interval = '1d'

    df = ticker.history(interval=interval, auto_adjust=True,
                        start=start, end=end)

    days = df.index.strftime('%m-%d')
    plt.figure(figsize=(10, 6))
    plt.plot(days, df['Open'], marker='.', color='red')
    plt.title(f'Open Price of {ticker} at 1 day between {start} and {end}')
    plt.xlabel('Date')
    plt.ylabel('Open Price')
    plt.grid(True)
    plt.show()


# 1m 차트
def week_chart(ticker,start, end):
    interval = '1mo'

    df = ticker.history(interval=interval, auto_adjust=True,
                        start=start, end=end)

    days = df.index.strftime('%Y-%m')
    plt.figure(figsize=(10, 6))
    plt.plot(days, df['Open'], marker='.', color='red')
    plt.title(f'Open Price of {ticker} at 1 week between {start} and {end}')
    plt.xlabel('Date')
    plt.ylabel('Open Price')
    plt.grid(True)
    plt.show()


# 1y 차트
def year_chart(ticker, start, end):
    interval = '3mo'

    df = ticker.history(interval=interval, auto_adjust=True,
                        start=start, end=end)

    days = df.index.strftime('%Y-%m')
    plt.figure(figsize=(10, 6))
    plt.plot(days, df['Open'], marker='.', color='red')
    plt.title(f'Open Price of {ticker} at 1 year  between {start} and {end}')
    plt.xlabel('Date')
    plt.ylabel('Open Price')
    plt.grid(True)
    plt.show()
