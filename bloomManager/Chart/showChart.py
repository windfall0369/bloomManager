import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# 1d 차트
def day_chart(ticker, start, end):
    interval = '1d'

    df = ticker.history(interval=interval, auto_adjust=True,
                        start=start, end=end)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))
    fig.update_traces(increasing_line_color='red', decreasing_line_color='blue')
    dailyChartImg = fig.to_image(format='png')

    return dailyChartImg


# 1m 차트
def week_chart(ticker, start, end):
    interval = '5d'

    df = ticker.history(interval=interval, auto_adjust=True,
                        start=start, end=end)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))
    fig.update_traces(increasing_line_color='red', decreasing_line_color='blue')
    weekChartImg = fig.to_image(format='png')

    return weekChartImg


# 1y 차트
def month_chart(ticker, start, end):
    interval = '1mo'

    df = ticker.history(interval=interval, auto_adjust=True,
                        start=start, end=end)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))
    fig.update_traces(increasing_line_color='red', decreasing_line_color='blue')
    monthChartImg = fig.to_image(format='png')

    return monthChartImg
