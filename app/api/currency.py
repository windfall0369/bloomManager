import yfinance as yf
from fastapi import FastAPI, APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import pandas as pd
from fredapi import Fred

router = APIRouter(
    prefix="/currency",
    tags=["currency"]
)
app = FastAPI()

templates = Jinja2Templates(directory="templates")


# 1 달러 -> 원화
@router.get("/USD/KRW")
def get_usd_krw(request: Request):
    ticker = yf.Ticker('USDKRW=X')

    df = ticker.history()
    today_close = df['Close'].iloc[-1]

    return today_close


# 1 달러 -> 엔화
@router.get('/USD/JPY')
def get_usd_jpy(request: Request):
    ticker = yf.Ticker('JPY=X')
    df = ticker.history()
    today_close = df['Close'].iloc[-1]

    return today_close


# 1 달러 -> 유로
@router.get('/USD/EUR')
def get_usd_eur(request: Request):
    ticker = yf.Ticker('EUR=X')
    df = ticker.history()
    today_close = df['Close'].iloc[-1]

    return today_close


@router.get('/KRW/JPY')
def get_krw_jpy(request: Request):
    ticker = yf.Ticker('KRWJPY=X')
    df = ticker.history()
    today_close = df['Close'].iloc[-1]

    return today_close


@router.get('/KRW/EUR')
def get_krw_eur(request: Request):
    ticker = yf.Ticker('KRWEUR=X')
    df = ticker.history()
    today_close = df['Close'].iloc[-1]

    return today_close


@router.get('/KRW/UDS')
def get_krw_usd(request: Request):
    ticker = yf.Ticker('KRWUSD=X')
    df = ticker.history()
    today_close = df['Close'].iloc[-1]

    return today_close
