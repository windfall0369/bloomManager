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
app = FastAPI()

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


options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option('detach', True)

# driver = webdriver.Chrome(options=options)

# url = 'https://naver.com'
fred = Fred(api_key='10eaeb34719b8137e832acfc3d79d714')
data = fred.get_series('SP500', '2023-01-01', '2024-01-01')
print(data)
