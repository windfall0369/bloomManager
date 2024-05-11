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

# 티커리스트 불러오기
ticker_list = pd.read_sql("""
select * from global_ticker
where date = (select max(date) from global_ticker)
and country = 'United States';
""", con=engine)

# DB 저장 쿼리
query = """
    insert into global_price (Date, High, Low, Open, Close, Volume, `Adj Close`, ticker)
    values (%s, %s,%s,%s,%s,%s,%s,%s) as new
    on duplicate key update
    High = new.High, Low = new.Low, Open = new.Open, Close = new.Close,
    Volume = new.Volume, `Adj Close` = new.`Adj Close`;
"""

error_list = []

# 전종목 주가 다운로드 및 저장
for i in tqdm(range(0, len(ticker_list))):
    ticker = ticker_list['Symbol'][i]
    try:

        # 주가 다운로드
        data = yf.download(ticker, progress=False)

        # 데이터 클렌징
        data['ticker'] = ticker

        data.to_sql('global_price', con=engine, if_exists='append', index = True,
                    index_label='Date')

    except:

        # 오류 발생시 error_list에 티커 저장하고 넘어가기
        print(ticker)
        error_list.append(ticker)

    # 타임슬립 적용
    time.sleep(2)

# 연결 종료
engine.dispose()
con.close()


print(error_list)