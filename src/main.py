from json import JSONDecodeError
from fastapi import FastAPI, Request, Response
from client import GettyClient
from pydantic import BaseModel
import requests

app = FastAPI()

class ProxyResponse(BaseModel):

    status_code: int
    request_url: str
    text: str
    json_response: str | None = None

@app.get("/proxy")
def proxy(url: str):
    response = requests.get(
        verify=False,
        url=url
    )
    try:
        json = response.json()
    except JSONDecodeError:
        json = None
    return ProxyResponse(
        status_code=response.status_code,
        text=response.text,
        request_url=response.request.url,
        json_response=json
    )
