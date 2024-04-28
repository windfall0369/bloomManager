import sys
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

from bloomManager.Chart import showChart

from bloomManager.FinancialsInfo import financial_info

name = 'MSFT'
ticker = yf.Ticker(name)
df = ticker.history(interval='5d', auto_adjust=True,
                    period='1y', start='2024-01-01')

# 인자로 ticker 넘겨서 정보 계속 받아옴
financialReader = financial_info.Financial()
# showChart.day_chart(ticker, '2020-01-01', '2020-12-31')
# showChart.week_chart(ticker, '2020-01-01', '2020-12-31')
showChart.year_chart(ticker, '2020-01-01', '2023-01-01')
