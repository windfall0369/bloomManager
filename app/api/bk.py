import numpy as np
import pandas as pd
from bokeh.io import output_file

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool, CrosshairTool, Range1d, RangeTool
from bokeh.plotting import figure, show
import yfinance as yf

# yfinance를 사용하여 주식 데이터 가져오기
ticker = yf.Ticker('AAPL')
df = ticker.history(start='2010-01-01', end='2023-12-31', interval='1d', auto_adjust=True)

# ColumnDataSource 생성
source = ColumnDataSource(data={
    'date': df.index,  # 인덱스를 사용합니다.
    'close': df['Close'],
    'open': df['Open'],
    'high': df['High'],
    'low': df['Low'],
})

# figure 생성
p = figure(x_axis_type="datetime", title="AAPL Close 가격",
           x_axis_label='날짜', y_axis_label='Close 가격', tools="pan,box_zoom,reset,save")

# close 가격을 선으로 플로팅
p.line(x='date', y='close', source=source, legend_label='Close', line_width=2, color='blue')

# HoverTool 설정
hover = HoverTool(
    tooltips=[
        ('Date', '@date{%F}'),
        ('Open', '@open'),
        ('High', '@high'),
        ('Low', '@low'),
    ],
    formatters={'@date': 'datetime'},
    mode='vline'
)
p.add_tools(hover)

# 그래프 외의 가격들은 그래프에 포함되지 않도록 범위를 설정
p.y_range = Range1d(df['Low'].min(), df['High'].max())

# CrosshairTool 생성 및 설정
crosshair = CrosshairTool(line_color='black', line_alpha=0.8, line_width=0.7)
p.add_tools(crosshair)

# RangeTool 생성
select = figure(title="Drag the middle and edges of the selection box to change the range above",
                height=130, width=800, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")

range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2

select.line('date', 'close', source=source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)

# 차트 출력
output_file("stock_chart.html")
show(column(p, select))
