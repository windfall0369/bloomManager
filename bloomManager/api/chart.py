import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from fastapi.responses import *
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
import mplfinance as mpf


router = APIRouter(
    prefix="/chart",
    tags=["chart"]

)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def daily_chart(ticker, today):
    interval = '30m'
    # str -> datetime 변환 후 +1일
    end_date = datetime.strptime(today, '%Y-%m-%d') + timedelta(days=1)

    df = ticker.history(interval=interval, auto_adjust=True, period='1d',
                        start=today, end=end_date)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))
    fig.update_traces(increasing_line_color='red', decreasing_line_color='blue')
    dailyChartImg = fig.to_image(format='png')

    return dailyChartImg


def day_chart(ticker, start, end):
    interval = '1d'

    df = ticker.history(interval=interval, auto_adjust=True,
                        start=start, end=end)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))
    fig.update_traces(increasing_line_color='red', decreasing_line_color='blue')
    dayChartImg = fig.to_image(format='png')

    return dayChartImg


# 1m 차트
def week_chart(ticker, start, end):
    interval = '5d'

    df = ticker.history(interval=interval, auto_adjust=True,
                        start=start, end=end)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))
    fig.update_traces(increasing_line_color='red', decreasing_line_color='blue')
    weekChartImg = fig.to_image(format='png')

    return weekChartImg


# 1y 차트
def month_chart(ticker, start, end):
    interval = '1mo'

    df = ticker.history(interval=interval, auto_adjust=True,
                        start=start, end=end)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))
    fig.update_traces(increasing_line_color='red', decreasing_line_color='blue')
    monthChartImg = fig.to_image(format='png')

    return monthChartImg


@router.get("/daily/{name}")
def get_daily_chart(name: str):
    ticker = yf.Ticker(name)
    img = daily_chart(ticker, '2024-04-19')

    return Response(content=img, media_type='image/png')


@router.get("/day/{name}")
def get_day_chart(name: str):
    ticker = yf.Ticker(name)
    img = day_chart(ticker, '2024-01-01', '2024-12-31')

    return Response(content=img, media_type='image/png')


@router.get("/week/{name}")
def get_week_chart(name: str):
    ticker = yf.Ticker(name)
    img = week_chart(ticker, '2024-01-01', '2024-12-31')

    return Response(content=img, media_type='image/png')


@router.get("/month/{name}")
def get_month_chart(name: str):
    ticker = yf.Ticker(name)
    img = month_chart(ticker, '2024-01-01', '2024-12-31')

    return Response(content=img, media_type='image/png')
