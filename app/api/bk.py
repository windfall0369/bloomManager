import numpy as np
import pandas as pd
from bokeh.embed import components
from bokeh.io import output_file

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool, CrosshairTool, Range1d, RangeTool, DatetimeTickFormatter, \
    DatetimeTicker, Span, NumeralTickFormatter
from bokeh.plotting import figure, show
import yfinance as yf


def draw_stock_chart(symbol, start_date, end_date, interval):
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start_date, end=end_date, interval=interval,
                        auto_adjust=True)

    # # 이동평균 계산
    df['MA60'] = df['Close'].rolling(window=60).mean()
    df['MA120'] = df['Close'].rolling(window=120).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()

    source = ColumnDataSource(data={
        'date': df.index,
        'close': df['Close'],
        'open': df['Open'],
        'high': df['High'],
        'low': df['Low'],
        'volume': df['Volume'],
        'MA60': df['MA60'],
        'MA120': df['MA120'],
        'MA200': df['MA200']

    })

    p = figure(x_axis_type="datetime", title=f"{symbol} Close 가격",
               width=1200, height=300,
               background_fill_color="#051221",
               tools="pan,box_zoom,reset,save")

    p.xaxis.formatter = DatetimeTickFormatter(
        years="%Y"
    )
    p.xaxis.major_label_orientation = 3.14 / 4  # 라벨을 대각선으로 설정
    p.xaxis.ticker = DatetimeTicker(desired_num_ticks=15)

    # close 가격을 선으로 플로팅
    p.line(x='date', y='close', source=source,
           legend_label='Close', line_width=1.2, line_alpha=0.9,
           color='#c34142')

    # 이동평균선 추가
    p.line(x='date', y='MA60', source=source,
           legend_label='MA60', line_width=0.7, line_alpha=0.8,
           color='#4286f4')

    p.line(x='date', y='MA120', source=source,
           legend_label='MA120', line_width=0.4, line_alpha=0.8,
           color='yellow')

    p.line(x='date', y='MA200', source=source,
           legend_label='MA200', line_width=0.7, line_alpha=0.8,
           color='#f442c2')

    # legend 설정
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.legend.label_text_font_size = "10pt"
    p.legend.glyph_width = 15
    p.legend.glyph_height = 15
    p.legend.spacing = 5

    # 격자선 제거
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = '#121a24'

    # HoverTool 설정
    hover = HoverTool(
        tooltips=[
            ('Date', '@date{%F}'),
            ('Open', '@open'),
            ('High', '@high'),
            ('Low', '@low'),
            ('Volume', '@volume'),
        ],
        formatters={'@date': 'datetime'},
        mode='vline'
    )
    p.add_tools(hover)

    # 그래프 외의 가격들은 그래프에 포함되지 않도록 범위를 설정
    p.y_range = Range1d(df['Low'].min(), df['High'].max())

    # CrosshairTool 생성 및 설정

    width = Span(location=0, dimension="width", line_dash="dashed", line_width=0.7, line_alpha=0.8,
                 line_color='#6a717a')
    height = Span(location=0, dimension="height", line_dash="dotted", line_width=0.7, line_alpha=0.8,
                  line_color='#6a717a')

    crosshair = CrosshairTool(overlay=[width, height])
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

    volume_source = ColumnDataSource(
        data={
            'date': df.index,
            'volume': df['Volume']
        })

    #################################################

    # figure 생성
    q = figure(x_axis_type='datetime', title="AAPL 거래량",
               width=1200, height=250,
               background_fill_color="#0A1B33",
               tools="")

    q.xaxis.formatter = DatetimeTickFormatter(
        years="%Y"
    )
    q.xaxis.major_label_orientation = 3.14 / 4  # 라벨을 대각선으로 설정
    q.xaxis.ticker = DatetimeTicker(desired_num_ticks=15)

    q.vbar(x='date', top='volume', source=volume_source,
           legend_label='Volume', line_width=1.2, color='#FF5733', line_alpha=0.9)

    q.legend.location = "top_left"
    q.legend.click_policy = "hide"
    q.legend.label_text_font_size = "10pt"
    q.legend.glyph_width = 15
    q.legend.glyph_height = 15
    q.legend.spacing = 5

    q.xgrid.grid_line_color = None
    q.ygrid.grid_line_color = None

    q.yaxis.formatter = NumeralTickFormatter(format="0,0")

    # HoverTool 설정
    hover_volume = HoverTool(
        tooltips=[
            ('Date', '@date{%F}'),
            ('Volume', '@volume{0,0}')
        ],
        formatters={
            '@date': 'datetime',
        },
        mode='vline'
    )

    q.add_tools(hover_volume)

    q.add_tools(crosshair)

    q.y_range = Range1d(df['Volume'].min(), df['Volume'].max())

    select_volume = figure(title="Drag the middle and edges of the selection box to change the range above",
                           height=130, width=800, y_range=q.y_range,
                           x_axis_type="datetime", y_axis_type=None,
                           tools="", toolbar_location=None, background_fill_color="#efefef")

    range_tool_v = RangeTool(x_range=q.x_range)
    range_tool_v.overlay.fill_color = "navy"
    range_tool_v.overlay.fill_alpha = 0.2

    select_volume.line('date', 'volume', source=source)
    select_volume.ygrid.grid_line_color = None
    select_volume.add_tools(range_tool_v)

    script, div = components(column(p, q, select, select_volume))

    return script, div


#
#
# # yfinance를 사용하여 주식 데이터 가져오기
# ticker = yf.Ticker('AAPL')
# df = ticker.history(start='2010-01-01', end='2023-12-31', interval='1d', auto_adjust=True)
#
# # 이동평균 계산
# df['MA60'] = df['Close'].rolling(window=60).mean()
# df['MA120'] = df['Close'].rolling(window=120).mean()
# df['MA200'] = df['Close'].rolling(window=200).mean()
#
# # ColumnDataSource 생성
# source = ColumnDataSource(data={
#     'date': df.index,
#     'close': df['Close'],
#     'open': df['Open'],
#     'high': df['High'],
#     'low': df['Low'],
#     'volume': df['Volume'],
#     'MA60': df['MA60'],
#     'MA120': df['MA120'],
#     'MA200': df['MA200']
#
# })
#
# p = figure(x_axis_type="datetime", title="AAPL Close 가격",
#            width=1200, height=300,
#            x_axis_label='날짜', y_axis_label='Close 가격',
#            background_fill_color="#051221",
#            tools="pan,box_zoom,reset,save")
#
# p.xaxis.formatter = DatetimeTickFormatter(
#     years="%Y"
# )
# p.xaxis.major_label_orientation = 3.14 / 4  # 라벨을 대각선으로 설정
# p.xaxis.ticker = DatetimeTicker(desired_num_ticks=15)
#
# # close 가격을 선으로 플로팅
# p.line(x='date', y='close', source=source,
#        legend_label='Close', line_width=1.2, line_alpha=0.9,
#        color='#c34142')
#
# # 이동평균선 추가
# p.line(x='date', y='MA60', source=source,
#        legend_label='MA60', line_width=0.7, line_alpha=0.8,
#        color='#4286f4')
#
# p.line(x='date', y='MA120', source=source,
#        legend_label='MA120', line_width=0.4, line_alpha=0.8,
#        color='yellow')
#
# p.line(x='date', y='MA200', source=source,
#        legend_label='MA200', line_width=0.7, line_alpha=0.8,
#        color='#f442c2')
#
# # legend 설정
# p.legend.location = "top_left"
# p.legend.click_policy = "hide"
# p.legend.label_text_font_size = "10pt"
# p.legend.glyph_width = 15
# p.legend.glyph_height = 15
# p.legend.spacing = 5
#
# # 격자선 제거
# p.xgrid.grid_line_color = None
# p.ygrid.grid_line_color = '#121a24'
#
# # HoverTool 설정
# hover = HoverTool(
#     tooltips=[
#         ('Date', '@date{%F}'),
#         ('Open', '@open'),
#         ('High', '@high'),
#         ('Low', '@low'),
#         ('Volume', '@volume'),
#     ],
#     formatters={'@date': 'datetime'},
#     mode='vline'
# )
# p.add_tools(hover)
#
# # 그래프 외의 가격들은 그래프에 포함되지 않도록 범위를 설정
# p.y_range = Range1d(df['Low'].min(), df['High'].max())
#
# # CrosshairTool 생성 및 설정
#
# width = Span(location=0, dimension="width", line_dash="dashed", line_width=0.7, line_alpha=0.8, line_color='#6a717a')
# height = Span(location=0, dimension="height", line_dash="dotted", line_width=0.7, line_alpha=0.8, line_color='#6a717a')
#
# crosshair = CrosshairTool(overlay=[width, height])
# p.add_tools(crosshair)
#
# # RangeTool 생성
# select = figure(title="Drag the middle and edges of the selection box to change the range above",
#                 height=130, width=800, y_range=p.y_range,
#                 x_axis_type="datetime", y_axis_type=None,
#                 tools="", toolbar_location=None, background_fill_color="#efefef")
#
# range_tool = RangeTool(x_range=p.x_range)
# range_tool.overlay.fill_color = "navy"
# range_tool.overlay.fill_alpha = 0.2
#
# select.line('date', 'close', source=source)
# select.ygrid.grid_line_color = None
# select.add_tools(range_tool)
#
# volume_source = ColumnDataSource(
#     data={
#         'date': df.index,
#         'volume': df['Volume']
#     })
#
# # figure 생성
# q = figure(x_axis_type='datetime', title="AAPL 거래량",
#            width=1200, height=250,
#            x_axis_label='날짜', y_axis_label='거래량',
#            background_fill_color="#0A1B33",
#            tools="")
#
# q.xaxis.formatter = DatetimeTickFormatter(
#     years="%Y"
# )
# q.xaxis.major_label_orientation = 3.14 / 4  # 라벨을 대각선으로 설정
# q.xaxis.ticker = DatetimeTicker(desired_num_ticks=15)
#
# q.vbar(x='date', top='volume', source=volume_source,
#        legend_label='Volume', line_width=1.2, color='#FF5733', line_alpha=0.9)
#
# q.legend.location = "top_left"
# q.legend.click_policy = "hide"
# q.legend.label_text_font_size = "10pt"
# q.legend.glyph_width = 15
# q.legend.glyph_height = 15
# q.legend.spacing = 5
#
# q.xgrid.grid_line_color = None
# q.ygrid.grid_line_color = None
#
# q.yaxis.formatter = NumeralTickFormatter(format="0,0")
#
# # HoverTool 설정
# hover_volume = HoverTool(
#     tooltips=[
#         ('Date', '@date{%F}'),
#         ('Volume', '@volume{0,0}')
#     ],
#     formatters={
#         '@date': 'datetime',
#     },
#     mode='vline'
# )
#
# q.add_tools(hover_volume)
#
# q.add_tools(crosshair)
#
# q.y_range = Range1d(df['Volume'].min(), df['Volume'].max())
#
# select_volume = figure(title="Drag the middle and edges of the selection box to change the range above",
#                        height=130, width=800, y_range=q.y_range,
#                        x_axis_type="datetime", y_axis_type=None,
#                        tools="", toolbar_location=None, background_fill_color="#efefef")
#
# range_tool_v = RangeTool(x_range=q.x_range)
# range_tool_v.overlay.fill_color = "navy"
# range_tool_v.overlay.fill_alpha = 0.2
#
# select_volume.line('date', 'volume', source=source)
# select_volume.ygrid.grid_line_color = None
# select_volume.add_tools(range_tool_v)
#
# # 차트 출력
# # output_file("stock_chart.html")
# # show(column(p, q, select, select_volume))
#
#
# # Bokeh 차트를 HTML 및 JavaScript 코드로 변환
# script, div = components(column(p, q, select, select_volume))
# print(type(script))
# print(type(div))
#

script, div = draw_stock_chart('AAPL', '2020-01-01', '2023-12-31', '1d')



# HTML 코드 생성
html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bokeh Chart</title>
    <link rel="stylesheet" href="https://cdn.bokeh.org/bokeh/release/bokeh-3.4.1.min.css" type="text/css" />
    <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-3.4.1.min.js"></script>
</head>
<body>
    {div}
    {script}
    
</body>
</html>
"""

# HTML 파일로 저장
with open("Func_Test.html", "w") as f:
    f.write(html)
