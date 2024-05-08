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
import requests
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

# FRED API Key
api_key = '10eaeb34719b8137e832acfc3d79d714'


# 셀레니움 크롤러
def sel_crawler(url, className):
    option = Options()
    option.add_argument("--headless")
    driver = webdriver.Chrome(options=option)
    driver.get(url)

    # 페이지가 완전히 로드될 때까지 기다립니다.
    time.sleep(2)  # 페이지 로딩에 필요한 시간을 적절히 조절합니다.

    # 요소가 나타날 때까지 대기합니다.
    element = None
    max_attempts = 10
    attempts = 0
    while attempts < max_attempts:
        try:
            element = driver.find_element(By.CLASS_NAME, className)
            break
        except:
            attempts += 1

    if element:
        score = element.text
    else:
        score = "Data not found"

    driver.quit()

    return score


def get_weekday(day):
    if day.weekday() > 5:
        return day
    else:
        while day.weekday() >= 5:
            day -= datetime.timedelta(days=1)
        return day


@router.get("/fear_and_greed")
def get_fng():
    url = "https://edition.cnn.com/markets/fear-and-greed"
    className = "market-fng-gauge__dial-number-value"
    fng = sel_crawler(url, className)
    return {"fng_score": fng}


def get_fred_daily(ticker):
    fred = Fred(api_key)
    score = fred.get_series(ticker)
    today = score.index[-1]
    today = today.strftime('%Y-%m-%d')
    score = score.iloc[-1]

    return {today: score}


@router.get('/NASDAQCOM/Today')
def get_NASDAQCOM():
    return get_fred_daily('NASDAQCOM')


@router.get("/DJI/Today")
def get_DJI_Daily():
    return get_fred_daily('DJI')


@router.get('/SP500/Today')
def get_SP500_Daily():
    return get_fred_daily('SP500')


@router.get('/DJI')
def get_DJI(start: str = None,
            end: str = None):
    fred = Fred(api_key)

    if end is None:
        end = date.today()

    DJI = fred.get_series('DJIA', start, end)

    df = DJI.to_frame(name='DJIA')
    df.index = pd.to_datetime(df.index)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['DJI'], mode='lines', name='DJI'))
    fig.update_layout(
        title="DJI Daily Data",
        title_font_size=20,
        xaxis_title="Date",
        yaxis_title="DJI",
        legend_title="Legend Title",
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(family="Courx`ier New, monospace", size=18, color="RebeccaPurple"),
        paper_bgcolor="white",
    )

    chart = fig.to_image(format='png')

    return Response(content=chart, media_type='image/png')


@router.get('/SP500')
def get_SP500(start: str = None,
              end: str = None):
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
        font=dict(family="Courx`ier New, monospace", size=18, color="RebeccaPurple"),
        paper_bgcolor="white",
    )

    chart = fig.to_image(format='png')

    return Response(content=chart, media_type='image/png')
