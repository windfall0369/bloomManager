import sys
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt



name = '005930.KS'
ticker = yf.Ticker(name)
df = ticker.history(interval='1d', period='1y', auto_adjust=False)

print(df.tail())
print(df.info())
