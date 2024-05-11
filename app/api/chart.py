import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from fastapi.responses import *
from fastapi import FastAPI, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
import mplfinance as mpf
import matplotlib

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.plotting import figure, show
from bokeh.sampledata.stocks import AAPL

from matplotlib.pyplot import show
import matplotlib.pyplot as plt
import io

# 커스텀 마켓 컬러 설정
chart_style = {
    "base_mpl_style": "dark_background",
    "marketcolors": {
        "candle": {"up": "#3dc985", "down": "#ef4f60"},
        "edge": {"up": "#3dc985", "down": "#ef4f60"},
        "wick": {"up": "#3dc985", "down": "#ef4f60"},
        "ohlc": {"up": "green", "down": "red"},
        "volume": {"up": "#247252", "down": "#82333f"},
        "vcedge": {"up": "green", "down": "red"},
        "vcdopcod": False,
        "alpha": 1,
    },
    "mavcolors": ("#ad7739", "#a63ab2", "#62b8ba"),
    "facecolor": "#1b1f24",
    "gridcolor": "#2c2e31",
    "gridstyle": "--",
    "y_on_right": True,
    "rc": {
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.edgecolor": "#474d56",
        "axes.titlecolor": "red",
        "figure.facecolor": "#161a1e",
        "figure.titlesize": "x-large",
        "figure.titleweight": "semibold",
    },
    "base_mpf_style": "binance-dark",
}

# 차트 출력x, 백엔드 'Agg' 사용
show(block=False)
matplotlib.use('Agg')

router = APIRouter(
    prefix="/chart",
    tags=["chart"]

)


templates = Jinja2Templates(directory="templates")


# mpf 활용
def draw_mpf(ticker, start, end, interval, style,
             volume: bool = True,
             mav: tuple = None):
    df = ticker.history(start=start, end=end,
                        interval=interval, auto_adjust=True,
                        )

    # chart_style로 커스텀 관리
    fig, axlist = mpf.plot(df,
                           type=style,
                           volume=volume,
                           returnfig=True,
                           style=chart_style,
                           mav=(20, 60, 120),
                           title=ticker.info['shortName'] + ' price \n between ' + str(start) + ' to ' + str(
                               end) + ' by ' + interval,
                           ylabel='Price ($)',
                           ylabel_lower=' Volume')
    fig.set_size_inches(18, 13)
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    chart = img_buffer.read()

    return chart


@router.get("/mpf/{name}")
def mpf_chart(name: str,
              start: str = '2024-01-01',
              end: str = '2024-12-31',
              interval: str = '1d',
              style: str = 'line'):
    ticker = yf.Ticker(name)

    img = draw_mpf(ticker, start=start, end=end, interval=interval, style=style)
    return Response(content=img, media_type='image/png')


@router.get("/daily/{name}")
def get_daily_chart(name: str,
                    start: str = '2024-04-19',
                    end: str = '2024-04-20',
                    style: str = 'line'
                    ):
    interval: str = '1h'
    ticker = yf.Ticker(name)

    dailyChartImg = draw_mpf(ticker, start=start, end=end, interval=interval, style=style)

    return Response(content=dailyChartImg, media_type='image/png')


@router.get("/day/{name}")
def get_day_chart(name: str,
                  start: str = '2024-04-19',
                  end: str = '2024-04-26',
                  style: str = 'line',
                  ):
    interval = '1d'
    ticker = yf.Ticker(name)

    dayChartImg = draw_mpf(ticker, start=start, end=end, interval=interval, style=style)

    return Response(content=dayChartImg, media_type='image/png')


@router.get("/week/{name}")
def get_week_chart(name: str,
                   start: str = '2024-01-01',
                   end: str = '2024-12-31',
                   style: str = 'line'):
    interval = '5d'
    ticker = yf.Ticker(name)

    weekChartImg = draw_mpf(ticker, start=start, end=end, interval=interval, style=style)

    return Response(content=weekChartImg, media_type='image/png')


@router.get("/month/{name}")
def get_month_chart(name: str,
                    start: str = '2024-01-01',
                    end: str = '2024-12-31',
                    style: str = 'line'):
    interval = '1mo'
    ticker = yf.Ticker(name)

    monthChartImg = draw_mpf(ticker, start=start, end=end, interval=interval, style=style)
    return Response(content=monthChartImg, media_type='image/png')








