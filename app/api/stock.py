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

router = APIRouter(
    prefix="/Stock",
    tags=["Stock"]
)
app = FastAPI()


templates = Jinja2Templates(directory="templates")


@router.get('/', response_class=HTMLResponse)
def get_stock(request: Request):
    return templates.TemplateResponse('stock.html', {'request': request})

