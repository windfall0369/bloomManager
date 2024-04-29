import sys

read = sys.stdin.readline


def call_list(ticker, date):
    opt = ticker.opt_chain(date)
    print(opt.calls.head())


def put_list(ticker, date):
    opt = ticker.opt_chain(date)
    print(opt.puts.head())


def call_list_all(ticker, date):
    opt = ticker.opt_chain(date)
    print(opt.calls[0:len(opt.calls)])


def put_list_all(ticker, date):
    opt = ticker.opt_chain(date)
    print(opt.puts[0:len(opt.puts)])

