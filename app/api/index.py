from datetime import date
import datetime
from pytimekr import pytimekr
import yfinance as yf
from fastapi import FastAPI, APIRouter
from fastapi import Request
from fastapi.responses import *
from fastapi.templating import Jinja2Templates
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import mplfinance as mpf
import time
import io
from bs4 import BeautifulSoup
import pandas as pd
from fredapi import Fred
import plotly.graph_objects as go

router = APIRouter(
    prefix="/index",
    tags=["index"]
)
app = FastAPI()

templates = Jinja2Templates(directory="templates")

api_key = '10eaeb34719b8137e832acfc3d79d714'


def get_weekday(date):
    if date.weekday() > 5:
        return date
    else:
        while date.weekday() >= 5:
            date -= datetime.timedelta(days=1)
        return date


@router.get('/SP500')
def get_SP500():
    fred = Fred(api_key)
    today = get_weekday(date.today())
    sp500 = fred.get_series('SP500', today)
    return sp500


@router.get('/SP500/Daily')
def get_SP500_Daily(start: str = None, end: str = None):
    fred = Fred(api_key)

    if end is None:
        end = date.today()

    sp500 = fred.get_series('SP500', start, end)

    df = sp500.to_frame(name='SP500')
    df.index = pd.to_datetime(df.index)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['SP500'], mode='lines', name='SP500'))
    fig.update_layout(
        title="SP500 Daily Data",
        title_font_size=20,
        xaxis_title="Date",
        yaxis_title="SP500",
        legend_title="Legend Title",
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(family="Courier New, monospace", size=18, color="RebeccaPurple"),
        paper_bgcolor="white",
    )

    chart = fig.to_image(format='png')

    return Response(content=chart, media_type='image/png')
