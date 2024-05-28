import yfinance as yf
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import *
from fastapi.templating import Jinja2Templates
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import pandas as pd
from fredapi import Fred
import requests

router = APIRouter(
    prefix="/news",
    tags=["news"]
)
app = FastAPI()

templates = Jinja2Templates(directory="templates")


@router.get('/', response_class=HTMLResponse)
def get_news(request: Request):
    return templates.TemplateResponse('news.html', {'request': request})


def get_news_list():
    URL = "https://www.hankyung.com/globalmarket/news-globalmarket"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    
