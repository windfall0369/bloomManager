import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from fastapi.responses import *
from fastapi import FastAPI, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
import mplfinance as mpf
import matplotlib

matplotlib.use('Agg')
from matplotlib.pyplot import show
import matplotlib.pyplot as plt
import io

from PIL import Image
from pathlib import Path

show(block=False)

router = APIRouter(
    prefix="/chart",
    tags=["chart"]

)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# 1일 뒤
# end_date = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)

def draw_chart(ticker, start, end, interval):
    df = ticker.history(interval=interval, auto_adjust=True,
                        start=start, end=end)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))
    fig.update_traces(increasing_line_color='red', decreasing_line_color='blue')
    chart = fig.to_image(format='png')

    return chart


def draw_mpf(ticker, start, end, interval):
    df = ticker.history(interval=interval, auto_adjust=True,
                        start=start, end=end)

    fig, axlist = mpf.plot(df, type='line', volume=True, returnfig=True)
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    chart_bytes = img_buffer.read()

    return chart_bytes


def draw_chart2(ticker,
                start: str = [None, '2024-01-01'],
                end: str = None,
                period: str = '1y',
                interval: str = '1d',
                style: str = 'line',
                volume: bool = True,
                mav=None):
    if end is None:
        end = datetime.strptime(start, '%Y-%m-%d') + timedelta(days=1)

    df = ticker.history(interval=interval, start=start, end=end,
                        period='1y', auto_adjust=True)

    fig, axlist = mpf.plot(df,
                           type=style,
                           volume=volume,
                           mav=(5, 30, 100),
                           returnfig=True)

    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    chart_bytes = img_buffer.read()

    return chart_bytes


@router.get("/mpf/{name}")
def mpf_chart(name: str):
    ticker = yf.Ticker(name)
    # df = ticker.history(ticker, interval='1d', auto_adjust=True, start='2023-01-01')

    img = draw_mpf(ticker, start='2023-01-01', end='2024-01-01', interval='1d')
    return Response(content=img, media_type='image/png')


@router.get("/daily/{name}")
def get_daily_chart(name: str, start: str = '2024-04-19', end: str = '2024-04-20'):
    ticker = yf.Ticker(name)

    dailyChartImg = draw_chart(ticker, start, end, '1h')

    return Response(content=dailyChartImg, media_type='image/png')


@router.get("/day/{name}")
def get_day_chart(name: str, start: str = '2024-04-19', end: str = '2024-04-26'):
    ticker = yf.Ticker(name)

    dayChartImg = draw_chart(ticker, start, end, '1d')

    return Response(content=dayChartImg, media_type='image/png')


@router.get("/week/{name}")
def get_week_chart(name: str, start: str = '2024-01-01', end: str = '2024-12-31'):
    ticker = yf.Ticker(name)

    weekChartImg = draw_chart(ticker, start, end, '5d')

    return Response(content=weekChartImg, media_type='image/png')


@router.get("/month/{name}")
def get_month_chart(name: str, start: str = '2024-01-01', end: str = '2024-12-31'):
    ticker = yf.Ticker(name)

    monthChartImg = draw_chart(ticker, start, end, '1mo')

    return Response(content=monthChartImg, media_type='image/png')
