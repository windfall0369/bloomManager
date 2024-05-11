from datetime import datetime

import yfinance as yf
from fastapi import FastAPI, APIRouter
from fastapi import Request
from fastapi.responses import *
from fastapi.templating import Jinja2Templates
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import pandas as pd
from fredapi import Fred


router = APIRouter(
    prefix="/raw_material",
    tags=["raw_material"]
)

templates = Jinja2Templates(directory="templates")


@router.get('/gold')
def get_gc(request: Request, start: str = '2023-01-01',
           end: str = '2023-12-31', interval: str = '1d',
           ):
    ticker = yf.Ticker('GC=F')

    # 금 선물 만기 출력
    expiry = ticker.info.get('expireDate')
    expire_date = datetime.utcfromtimestamp(expiry).strftime('%Y-%m-%d')
    print('만기 : ', expire_date)

    df = ticker.history(start=start, end=end, interval=interval)
    html_text = df.to_html(justify='center')
    html = open("./templates/gold.html", 'w')
    html.write(html_text)
    html.close()
    return templates.TemplateResponse('gold.html', {"request": request})


@router.get("/gold/chart")
def get_gold_chart(start: str = '2023-01-01',
                   end: str = '2023-12-31',
                   interval: str = '1d'):
    ticker = yf.Ticker('GC=F')



@router.get('/oil')
def get_oil(request: Request,
            start: str = '2023-01-01',
            end: str = '2023-12-31',
            interval: str = '1d'):
    ticker = yf.Ticker('CL=F')

    expiry = ticker.info['expireDate']
    expire_date = datetime.utcfromtimestamp(expiry).strftime('%Y-%m-%d')

    df = ticker.history(start=start, end=end, interval=interval)
    html_text = df.to_html(justify='center')
    html = open("./templates/oil.html", 'w')
    html.write(html_text)
    html.close()

    return templates.TemplateResponse('oil.html', {"request": request})


@router.get('/oil/chart')
def get_oil_chart(request: Request,
                  start: str = '2023-01-01',
                  end: str = '2023-12-31',
                  interval: str = '1d'):
    ticker = yf.Ticker('CL=F')
    df = ticker.history(start=start, end=end, interval=interval)
