from datetime import datetime
import datetime
import statsmodels.api as sm

import yfinance as yf
import pandas as pd
import famafrench

tickers = ['^KS11', '039490.KS']

all_data = {}
for ticker in tickers:
    all_data[ticker] = yf.download(ticker,
                                   start='2016-01-01',
                                   end='2024-05-13')

prices = pd.DataFrame({tic: data['Close'] for tic, data in all_data.items()})
ret = prices.pct_change().dropna()

# 절편 설정
ret['intercept'] = 1
# 선형회귀
reg = sm.OLS(ret[['039490.KS']], ret[['^KS11', 'intercept']]).fit()

# Dep. Variable : 종속변수 (개별 주식)
# intercept값이 알파(초과수익률)
# coef : 베타값
# t value는 절대값 2가 넘으면 의미가 있음
# R-squared : 설명력
print(type(reg.summary()))


def get_beta(tickers, start, end):
    all_data = {}
    for ticker in tickers:
        all_data[ticker] = yf.download(ticker,
                                       start=start,
                                       end=end)

    prices = pd.DataFrame({tic:data['Close'] for tic, data in all_data.items()})
    ret = prices.pct_change().dropna()
    ret['intercept'] = 1
    reg = sm.OLS(ret[[tickers[0]]], ret[[tickers[1], 'intercept']]).fit()

    return reg.summary()


link = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Portfolios_Formed_on_BE-ME_CSV.zip'
