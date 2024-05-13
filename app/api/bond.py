from datetime import datetime
import datetime

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
    prefix="/bond",
    tags=["bond"]
)
app = FastAPI()

templates = Jinja2Templates(directory="templates")


def get_bond(symbol):
    today = datetime.date.today()
    ticker = yf.Ticker(symbol)

    df = ticker.history(start="2024-01-01", end=today)
    today_score = round(df['Close'].iloc[-1], 2)

    return today_score


@router.get("/3month")
def get_3month_bond():
    return get_bond('^IRX')


@router.get('/FVX')
def get_FVX_bond():
    return get_bond('^FVX')


@router.get('/TYX')
def get_TYX_bond():
    return get_bond('^TYX')
