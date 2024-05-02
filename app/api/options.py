import yfinance as yf
from fastapi import FastAPI, APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/options",
    tags=["options"]
)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@router.get("/call/list/{name}")
def get_call_list(request: Request, name: str, date: str = '2024-05-03'):
    ticker = yf.Ticker(name)
    opt = ticker.option_chain(date)
    call = opt.calls.head()

    # json 반환
    # call_list = df.to_json(orient='records')
    # view 만들어서 반환
    html_text = call.to_html(justify='center')
    html = open("./templates/call_list.html", 'w')
    html.write(html_text)
    html.close()

    return templates.TemplateResponse('call_list.html', {"request": request})


@router.get("/put/list/{name}")
def get_put_list(request: Request, name: str, date: str = '2024-05-03'):
    ticker = yf.Ticker(name)
    opt = ticker.option_chain(date)
    put = opt.puts.head()

    # json 반환
    # put_list = df.to_json(orient='records')
    # view 만들어서 반환
    html_text = put.to_html(justify='center')
    html = open("./templates/put_list.html", 'w')
    html.write(html_text)
    html.close()

    return templates.TemplateResponse('put_list.html', {"request": request})
