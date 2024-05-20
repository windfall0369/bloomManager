from datetime import datetime

import yfinance as yf
import pandas as pd
import json
from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import HTMLResponse
from yahooquery import Ticker

from api import chart
from api import financial_info
from api import options
from api import report
from api import index
from api import raw_material
from api import currency
from api import bond

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chart.router)
app.include_router(financial_info.router)
app.include_router(options.router)
app.include_router(report.router)
app.include_router(index.router)
app.include_router(raw_material.router)
app.include_router(currency.router)
app.include_router(bond.router)


templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@app.get("/price/{name}")
def get_price(request: Request, name: str,
              start: str = '2024-01-01',
              period: str = '1y',
              interval: str = '1d'):
    print(f"name = {name}")
    ticker = yf.Ticker(name)
    df = ticker.history(interval=interval, auto_adjust=True,
                        period=period, start=start)

    html_table = df.to_html()
    return HTMLResponse(content=html_table)

