import yfinance as yf
from fastapi import FastAPI, APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/financial_info",
    tags=["financial_info"]
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def balance(ticker):
    balance_sheet = ticker.balance_sheet
    return balance_sheet


def cashflow(ticker):
    cashflow_sheet = ticker.cashflow
    return cashflow_sheet


def income_statement(ticker):
    income_stmt = ticker.quarterly_income_stmt
    return income_stmt


@router.get('/{name}/cash')
def get_cashflow(name: str, request: Request):
    ticker = yf.Ticker(name)
    df = cashflow(ticker)

    html_text = df.to_html(justify='center')
    html = open("./templates/cashflow.html", 'w')
    html.write(html_text)
    html.close()

    return templates.TemplateResponse('cashflow.html', {"request": request})


@router.get('/{name}/balance')
def get_balance(name: str, request: Request):
    ticker = yf.Ticker(name)
    df = balance(ticker)

    html_text = df.to_html(justify='center')
    html = open("./templates/balance.html", 'w')
    html.write(html_text)
    html.close()

    return templates.TemplateResponse('balance.html', {"request": request})


@router.get('/{name}/income')
def get_income(name: str, request: Request):
    ticker = yf.Ticker(name)
    df = income_statement(ticker)

    html_text = df.to_html(justify='center')
    html = open("./templates/income.html", 'w')
    html.write(html_text)
    html.close()

    return templates.TemplateResponse('income.html', {"request": request})


@router.get('/{name}/news')
def get_news(name: str, request: Request):
    ticker = yf.Ticker(name)
    new_list = ticker.news
