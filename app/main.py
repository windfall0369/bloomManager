from datetime import datetime

import yfinance as yf
import pandas as pd
import json
from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.responses import HTMLResponse

from api import chart
from api import financial_info
from api import options
from api import report
from api import index
from api import raw_material

app = FastAPI()

app.include_router(chart.router)
app.include_router(financial_info.router)
app.include_router(options.router)
app.include_router(report.router)
app.include_router(index.router)
app.include_router(raw_material.router)

templates = Jinja2Templates(directory="templates")


class Ticker(BaseModel):
    ticker: str
    market: str


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


