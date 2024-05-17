import pandas as pd
import pymysql
import yfinance as yf
from sqlalchemy import create_engine
from tqdm import tqdm
import time
from yahooquery import Ticker
import numpy as np

# 시가총액 문자열을 숫자로 변환하는 함수 정의
def convert_market_cap_to_number(market_cap_str):
    if pd.isnull(market_cap_str):
        return np.nan
    factor = 1
    if market_cap_str.endswith('T'):
        factor = 1e12
    elif market_cap_str.endswith('B'):
        factor = 1e9
    elif market_cap_str.endswith('M'):
        factor = 1e6
    try:
        numeric_part = float(market_cap_str[:-1])
        return numeric_part * factor
    except ValueError:  # 숫자 변환에 실패한 경우 NaN 반환
        return np.nan


# # DB 연결
engine = create_engine('mysql+pymysql://root:12345678@127.0.0.1:3306/stock_db')
con = pymysql.connect(user='root',
                      passwd='12345678',
                      host='127.0.0.1',
                      db='stock_db',
                      charset='utf8')

mycursor = con.cursor()

# netincome, capitalStock, CashFlowFromContinuingOperatingActivities, totlaRevenue


# 분기 재무제표
global_fs = pd.read_sql("""
select * from global_fs
where freq = 'q'
and account in ('NetIncome', 'CapitalStock', 'CashFlowFromContinuingOperatingActivities', 'TotalRevenue')
""", con=engine)

# 티커 리스트
ticker_list = pd.read_sql("""
select Symbol as ticker, `Market Cap`, date from global_ticker
where date = (select max(date) from global_ticker);
""", con=engine)

# 시가총액 문자열을 숫자로 변환
ticker_list['Market Cap'] = ticker_list['Market Cap'].apply(convert_market_cap_to_number)


# TTM
global_fs = global_fs.sort_values(['ticker', 'account', 'date'])
global_fs['ttm'] = global_fs.groupby(['ticker', 'account'], as_index=False)['value'].rolling(
    window=4, min_periods=4).sum()['value']

# 자본금 평균
global_fs['ttm'] = np.where(global_fs['account'] == 'CapitalStock', global_fs['ttm'] / 4,
                            global_fs['ttm'])
global_fs = global_fs.groupby(['account', 'ticker']).tail(1)


global_fs_merge = global_fs[['account', 'ticker',
                             'ttm']].merge(ticker_list[['ticker', 'Market Cap', 'date']],
                                           on='ticker')
# 형 변환
global_fs_merge['Market Cap'] = pd.to_numeric(global_fs_merge['Market Cap'], errors='coerce')

global_fs_merge['Market Cap'] = global_fs_merge['Market Cap']

global_fs_merge['value'] = global_fs_merge['Market Cap']/global_fs_merge['ttm']
global_fs_merge['value'] = global_fs_merge['value'].round(4)
global_fs_merge['indicator'] = np.where(
    global_fs_merge['account'] == 'TotalRevenue', 'PSR',
    np.where(
        global_fs_merge['account'] == 'CashFlowFromContinuingOperatingActivities','PCR',
        np.where(global_fs_merge['account'] == 'CapitalStock','PBR',
                 np.where(global_fs_merge['account'] == 'NetIncome', 'PER', None))))

global_fs_merge.rename(columns={'value' : 'value'}, inplace=True)
global_fs_merge = global_fs_merge[['ticker', 'date', 'indicator', 'value']]
global_fs_merge = global_fs_merge.replace([np.inf, -np.inf, np.nan], None)

# 값 확인
aapl_values = global_fs_merge.query("ticker == 'AAPL'")
print(aapl_values)

query = """
    insert into global_value (ticker, date, indicator, value)
    values (%s,%s,%s,%s) as new
    on duplicate key update
    value=new.value
"""

args_fs = global_fs_merge.values.tolist()
mycursor.executemany(query, args_fs)
con.commit()


global_fs = pd.read_sql("""
select * from global_fs
where freq = 'q'
and account in ('NetIncome', 'CapitalStock', 'CashFlowFromContinuingOperatingActivities', 'TotalRevenue', 'CommonStockDividendPaid', 'CommonStockPayments')
""", con=engine)


# 연결 종료
engine.dispose()
con.close()
