import math
from datetime import datetime

import numpy as np
import yfinance as yf
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy import create_engine
import pandas as pd
import pymysql
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# DB 연결

engine = create_engine('mysql+pymysql://root:12345678@127.0.0.1:3306/stock_db')
con = pymysql.connect(user='root',
                      passwd='12345678',
                      host='127.0.0.1',
                      db='stock_db',
                      charset='utf8')
mycursor = con.cursor()

# ticker list 불러오기
ticker_list = pd.read_sql("""
select * from global_ticker
where date = (select max(date) from global_ticker)
and country = 'United States';
""", con=engine)

# DB 저장 쿼리
query = """
    insert into global_price (Date, Open, High, Low, Close, `Adj Close`, Volume, ticker)
    values (%s, %s, %s, %s, %s, %s, %s, %s)
    on duplicate key update 
    Open = values(Open), High = values(High), Low = values(Low),
    Close = values(Close), `Adj Close` = values(`Adj Close`),
    Volume = values(Volume);
"""

error_list = []

for i in tqdm(range(0, len(ticker_list))):

    ticker = ticker_list['Symbol'][i]

    try:
        price = yf.download(ticker, progress=False)

        price = price.reset_index()
        price['ticker'] = ticker

        args = price.values.tolist()

        mycursor.executemany(query, args)
        con.commit()


    except Exception as e:
        print(f"Error for ticker {ticker}: {e}")
        error_list.append(ticker_list)

    time.sleep(2)

engine.dispose()
con.close()