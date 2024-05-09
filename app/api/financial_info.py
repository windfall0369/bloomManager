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


@router.get('/cash/{name}')
def get_cashflow(name: str, request: Request):
    ticker = yf.Ticker(name)
    df = ticker.cashflow

    html_text = df.to_html(justify='center')
    html = open("./templates/cashflow.html", 'w')
    html.write(html_text)
    html.close()

    return templates.TemplateResponse('cashflow.html', {"request": request})


@router.get('/balance/{name}')
def get_balance(name: str, request: Request):
    ticker = yf.Ticker(name)
    df = ticker.balance_sheet

    html_text = df.to_html(justify='center')
    html = open("./templates/balance.html", 'w')
    html.write(html_text)
    html.close()

    return templates.TemplateResponse('balance.html', {"request": request})


@router.get('/income/{name}')
def get_income(name: str, request: Request):
    ticker = yf.Ticker(name)
    df = ticker.quarterly_income_stmt

    html_text = df.to_html(justify='center')
    html = open("./templates/income.html", 'w')
    html.write(html_text)
    html.close()

    return templates.TemplateResponse('income.html', {"request": request})


@router.get('/news/{name}')
def get_news(name: str, request: Request):
    ticker = yf.Ticker(name)
    news_list = ticker.news

    return news_list

@router.get("/reco/{name}")
def get_reco(name: str, request: Request):
    ticker = yf.Ticker(name)

