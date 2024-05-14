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


def get_index(symbol):
    ticker = yf.Ticker(symbol)
    today = datetime.date.today()
    df = ticker.history(start='2024-01-01', end=today, interval='1d')
    today_score = round(df['Close'].iloc[-1], 2)

    return today_score


def get_index_chart(symbol):
    ticker = yf.Ticker(symbol)


@router.get('/SP500/chart')
def get_SP500(start: str = None,
              end: str = None):
    fred = Fred(api_key)

    if end is None:
        end = date.today()

    sp500 = fred.get_series('SP500', start, end)

    df = pd.DataFrame({'Date': sp500.index, 'SP500': sp500.values})

    fig = go.Figure()

    # 데이터프레임에서 Trace 추가
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SP500'], mode='lines', name='SP5000'))

    # 레이아웃 업데이트
    fig.update_layout(
        title="SP500 Daily Data",
        title_font_size=20,
        xaxis_title="Date",
        yaxis_title="DJIA",
        legend_title="Legend Title",
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(family="Courier New, monospace", size=18, color="RebeccaPurple"),
        paper_bgcolor="white",
    )

    chart = fig.to_image(format='png')

    return Response(content=chart, media_type='image/png')


@router.get('/SP500')
def get_sp500():
    return get_index('^GSPC')


@router.get('/NASDAQCOM')
def get_NASDAQCOM():
    return get_index('^IXIC')


@router.get('/RUT')
def get_RUT():
    return get_index('^RUT')


@router.get('/DJIA')
def get_DJIA():
    return get_index('^DJI')
