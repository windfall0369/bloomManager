import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from bokeh.embed import components
from fastapi.responses import *
from fastapi import Request
from fastapi import FastAPI, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
import mplfinance as mpf
import matplotlib

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool, HoverTool
from bokeh.plotting import figure, show, output_file, save

from matplotlib.pyplot import show
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
    prefix="/{name}/chart",
    tags=["chart"]

)

templates = Jinja2Templates(directory="templates")


@router.get('/html')
def get_html(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})


# @router.get('/test')
def test_chart():
    ticker = yf.Ticker('AAPL')
    df = ticker.history(start='2023-01-01', end='2023-12-31', interval='1d')

    # df.reset_index(inplace=True)
    # source = ColumnDataSource(df)
    #
    # p = figure(x_axis_type="datetime", title="AAPL Stock Price", width=800, height=400)
    # p.xaxis.axis_label = "Date"
    # p.yaxis.axis_label = "Price (USD)"
    # p.line(x='Date', y='Close', line_width=2, source=source, legend_label='Close Price', color='navy')
    # p.scatter(x='Date', y='Close', size=5, source=source, color='navy', alpha=0.5)
    #
    # hover = HoverTool()
    # hover.tooltips = [('Date', '@Date{%F}'), ('Close', '@Close{0.2f}')]
    # hover.formatters = {'@Date': 'datetime'}
    # p.add_tools(hover)

    return 0


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


@router.get("/mpf")
def mpf_chart(name: str,
              start: str = '2024-01-01',
              end: str = '2024-12-31',
              interval: str = '1d',
              style: str = 'line'):
    ticker = yf.Ticker(name)

    img = draw_mpf(ticker, start=start, end=end, interval=interval, style=style)
    return Response(content=img, media_type='image/png')


@router.get("/daily")
def get_daily_chart(name: str,
                    start: str = '2024-04-19',
                    end: str = '2024-04-20',
                    style: str = 'line'
                    ):
    interval: str = '1h'
    ticker = yf.Ticker(name)

    dailyChartImg = draw_mpf(ticker, start=start, end=end, interval=interval, style=style)

    return Response(content=dailyChartImg, media_type='image/png')


@router.get("/day")
def get_day_chart(name: str,
                  start: str = '2024-04-19',
                  end: str = '2024-04-26',
                  style: str = 'line',
                  ):
    interval = '1d'
    ticker = yf.Ticker(name)

    dayChartImg = draw_mpf(ticker, start=start, end=end, interval=interval, style=style)

    return Response(content=dayChartImg, media_type='image/png')


@router.get("/week")
def get_week_chart(name: str,
                   start: str = '2024-01-01',
                   end: str = '2024-12-31',
                   style: str = 'line'):
    interval = '5d'
    ticker = yf.Ticker(name)

    weekChartImg = draw_mpf(ticker, start=start, end=end, interval=interval, style=style)

    return Response(content=weekChartImg, media_type='image/png')


@router.get("/month")
def get_month_chart(name: str,
                    start: str = '2024-01-01',
                    end: str = '2024-12-31',
                    style: str = 'line'):
    interval = '1mo'
    ticker = yf.Ticker(name)

    monthChartImg = draw_mpf(ticker, start=start, end=end, interval=interval, style=style)
    return Response(content=monthChartImg, media_type='image/png')
