import pandas as pd
import pymysql
import yfinance as yf
from sqlalchemy import create_engine
from tqdm import tqdm
import time

# # DB 연결
engine = create_engine('mysql+pymysql://root:12345678@127.0.0.1:3306/stock_db')
con = pymysql.connect(user='root',
                      passwd='12345678',
                      host='127.0.0.1',
                      db='stock_db',
                      charset='utf8')

mycursor = con.cursor()

# 연결 종료
engine.dispose()
con.close()
