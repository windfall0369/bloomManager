from datetime import datetime

import yfinance as yf
import pandas as pd
import json
from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from api import chart
from api import financial_info
from api import options
from api import report
from api import index

app = FastAPI()


app.include_router(chart.router)
app.include_router(financial_info.router)
app.include_router(options.router)
app.include_router(report.router)
app.include_router(index.router)

templates = Jinja2Templates(directory="templates")

class Ticker(BaseModel):
    ticker: str
    market: str


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@app.get("/price/{name}")
def get_price(name: str):
    print(f"name = {name}")
    ticker = yf.Ticker(name)
    df = ticker.history(interval='1d', auto_adjust=True,
                        period='1y', start='2024-01-01')
    price = df.to_json(orient='records')
    print(type(price))
    print(price)
    data = json.loads(price)
    data = pd.json_normalize(data)
    print(data)

    return df.to_json(orient='records')
