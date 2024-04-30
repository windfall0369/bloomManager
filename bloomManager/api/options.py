import yfinance as yf
from fastapi import FastAPI, APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/options",
    tags= ["options"]
)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def call_list(ticker, date):
    opt = ticker.option_chain(date)
    call_list = opt.calls
    df = call_list.head()
    return df


def put_list(ticker, date):
    opt = ticker.option_chain(date)
    put_list = opt.puts
    df = put_list.head()
    return df


def call_list_all(ticker, date):
    opt = ticker.option_chain(date)
    print(opt.calls[0:len(opt.calls)])


def put_list_all(ticker, date):
    opt = ticker.option_chain(date)
    print(opt.puts[0:len(opt.puts)])


@router.get("/call/list/{name}")
def get_call_list(name: str, request: Request):
    ticker = yf.Ticker(name)
    date = '2024-05-03'
    df = call_list(ticker, date)

    # json 반환
    # call_list = df.to_json(orient='records')
    # view 만들어서 반환
    html_text = df.to_html(justify='center')
    html = open("./templates/call_list.html", 'w')
    html.write(html_text)
    html.close()

    return templates.TemplateResponse('call_list.html', {"request": request})


@router.get("/put/list/{name}")
def get_put_list(name: str, request: Request):
    ticker = yf.Ticker(name)
    date = '2024-05-03'
    df = put_list(ticker, date)

    # json 반환
    # put_list = df.to_json(orient='records')
    # view 만들어서 반환
    html_text = df.to_html(justify='center')
    html = open("./templates/put_list.html", 'w')
    html.write(html_text)
    html.close()

    return templates.TemplateResponse('put_list.html', {"request": request})
