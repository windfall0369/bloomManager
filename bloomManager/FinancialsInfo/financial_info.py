import sys

import yfinance as yf


class Financial():
    def balance(self, ticker):
        balance_sheet = ticker.balance_sheet
        print(balance_sheet)

    def cashflow(self, ticker):
        cashflow_sheet = ticker.cashflow
        print(cashflow_sheet)

    def income_statement(self, ticker):
        income_stmt = ticker.quarterly_income_stmt
        print(income_stmt)
