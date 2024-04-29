import sys
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import kaleido
from typing import Union
from fastapi import FastAPI
from fastapi.responses import *
from pydantic import BaseModel
import json
import io

from Chart import showChart
from FinancialsInfo import financial_info
from FutureOptions import calls_puts

app = FastAPI()


class Ticker(BaseModel):
    ticker: str
    market: str


@app.get("/")
async def read_root():
    return 'This is root path from MyAPI'


@app.get("/price/{name}")
def get_price(name: str):
    print(f"name = {name}")
    ticker = yf.Ticker(name)
    df = ticker.history(interval='1d', auto_adjust=True,
                        period='1y', start='2024-01-01')
    price = df.to_json(orient='records')
    print(type(price))
    print(price)
    data = json.loads(price)
    data = pd.json_normalize(data)
    print(data)

    return df.to_json(orient='records')


@app.get("/chart/day/{name}")
def get_chart(name: str):
    ticker = yf.Ticker(name)
    img = showChart.day_chart(ticker, '2024-01-01', '2024-12-31')

    return Response(content=img, media_type='image/png')


@app.get("/chart/week/{name}")
def get_chart(name: str):
    ticker = yf.Ticker(name)
    img = showChart.week_chart(ticker, '2024-01-01', '2024-12-31')

    return Response(content=img, media_type='image/png')


@app.get("/chart/month/{name}")
def get_chart(name: str):
    ticker = yf.Ticker(name)
    img = showChart.month_chart(ticker, '2024-01-01', '2024-12-31')

    return Response(content=img, media_type='image/png')
