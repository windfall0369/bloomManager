from datetime import datetime

import yfinance as yf
from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
import json

router = APIRouter(
    prefix="/financial_info",
    tags=["financial_info"]
)

templates = Jinja2Templates(directory="templates")


# 현금흐름표
@router.get('/cash')
def get_cashflow(name: str, request: Request):
    ticker = yf.Ticker(name)
    df = ticker.cashflow

    html_text = df.to_html(justify='center')
    html = open("./templates/cashflow.html", 'w')
    html.write(html_text)
    html.close()

    return templates.TemplateResponse('cashflow.html', {"request": request})


# 재무상태표
@router.get('/balance')
def get_balance(name: str, request: Request):
    ticker = yf.Ticker(name)
    df = ticker.balance_sheet

    html_text = df.to_html(justify='center')
    html = open("./templates/balance.html", 'w')
    html.write(html_text)
    html.close()

    return templates.TemplateResponse('balance.html', {"request": request})


# 손익계산서
@router.get('/income')
def get_income(name: str, request: Request):
    ticker = yf.Ticker(name)
    df = ticker.quarterly_income_stmt

    html_text = df.to_html(justify='center')
    html = open("./templates/income.html", 'w')
    html.write(html_text)
    html.close()

    return templates.TemplateResponse('income.html', {"request": request})


@router.get('/news')
def get_news(name: str, request: Request):
    ticker = yf.Ticker(name)
    news_list = ticker.news
    news_list = json.dumps(news_list)
    data = json.loads(news_list)
    news_items = []
    for item in data:
        title = item['title']
        publisher = item['publisher']
        providerPublishTime = datetime.utcfromtimestamp(item['providerPublishTime']).strftime('%Y-%m-%d')
        link = item['link']
        link = item['link']
        news_items.append({"title": title, "publisher": publisher, "providerPublishTime": providerPublishTime, "link": link})  # 링크 추가

    html_text = "<h1>News for {}</h1>".format(name)
    html_text += "<ul>"
    for item in news_items:
        html_text += "<li>"
        html_text += "<strong>Title:</strong> <a href='{}' target='_blank'>{}</a><br>".format(item["link"], item["title"])
        html_text += "<strong>Publisher:</strong> {}<br>".format(item["publisher"])
        html_text += "<strong>Provider Publish Time:</strong> {}<br>".format(item["providerPublishTime"])
        html_text += "</li>"
    html_text += "</ul>"

    with open("./templates/news_generated.html", 'w') as html_file:
        html_file.write(html_text)

    return templates.TemplateResponse("news_generated.html", {"request": request})

