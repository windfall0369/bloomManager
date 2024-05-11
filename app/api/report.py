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
    prefix="/report",
    tags=["report"]
)

templates = Jinja2Templates(directory="templates")


@router.get('/reco/{name}')
def get_recommendations(request: Request, name: str):
    ticker = yf.Ticker(name)
    reco = ticker.recommendations
    html_text = reco.to_html(justify='center')
    html = open("./templates/reco.html", 'w')
    html.write(html_text)
    html.close()
    return templates.TemplateResponse('reco.html', {"request": request})


