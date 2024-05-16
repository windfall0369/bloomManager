import yfinance as yf
from fastapi import FastAPI, APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import statsmodels.api as sm


router = APIRouter(
    prefix="/pick",
    tags=["pick"]
)
app = FastAPI()

templates = Jinja2Templates(directory="templates")


def get_beta(symbol, market):
    tickers = [symbol,market]
    all_data = {}
    ticker1 = yf.Ticker(symbol)
    df1 = ticker1.history(start="1900-01-01", end="2024-12-31", interval='1d',
                          auto_adjust=True)
    ticker2 = yf.Ticker(market)
    df2 = ticker2.history(start="1900-01-01", end="2024-12-31", interval='1d',
                          auto_adjust=True)

    for ticker in tickers:
        all_data[ticker] = yf.download(ticker,
                                       start="1900-01-01", end="2024-12-31",
                                       interval='1d', auto_adjust=True)

