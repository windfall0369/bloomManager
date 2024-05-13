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


def get_info(request, name, start, end, interval):
    ticker = yf.Ticker(name)

    expiry = ticker.info.get('expireDate')
    expire_date = datetime.utcfromtimestamp(expiry).strftime('%Y-%m-%d')

    # 티커 이름 매핑
    name_mapping = {
        'GC=F': 'gold',
        'CL=F': 'oil',
        'HG=F': 'copper',
        'SI=F': 'silver',
    }

    if name in name_mapping:
        name = name_mapping[name]

    df = ticker.history(start=start, end=end, interval=interval)
    html_text = f"<h2>만기일 : {expire_date}</h2>"
    html_text += df.to_html(justify='center')

    html = open(f"./templates/{name}.html", 'w')
    html.write(html_text)
    html.close()
    return templates.TemplateResponse(f'{name}.html', {"request": request})


@router.get('/gold')
def get_gc(request: Request, start: str = '2023-01-01',
           end: str = '2023-12-31', interval: str = '1d',
           ):
    return get_info(request, 'GC=F', start, end, interval)


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
    return get_info(request, 'CL=F', start, end, interval)


@router.get('/oil/chart')
def get_oil_chart(request: Request,
                  start: str = '2023-01-01',
                  end: str = '2023-12-31',
                  interval: str = '1d'):
    ticker = yf.Ticker('CL=F')
    df = ticker.history(start=start, end=end, interval=interval)


@router.get('/copper')
def get_copper(request: Request,
               start: str = '2023-01-01',
               end: str = '2023-12-31',
               interval: str = '1d'):
    return get_info(request, 'HG=F', start, end, interval)


@router.get('/silver')
def get_silver(request: Request,
               start: str = '2023-01-01',
               end: str = '2023-12-31',
               interval: str = '1d'):
    return get_info(request, 'SI=F', start, end, interval)
