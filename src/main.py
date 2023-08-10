from json import JSONDecodeError
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

origins = [
    "http://ohsmart.dansdemo.nl",
    "https://ohsmart.dansdemo.nl",
    "http://localhost:5489",
    "http://localhost:3000",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProxyResponse(BaseModel):

    request_url: str
    text: str
    json_response: str | None = None

@app.get("/proxy")
def proxy(url: str, response: Response):
    try:
        response = requests.get(
            verify=False,
            url=url
        )
    except requests.exceptions.ConnectionError:
        response.status_code=418
        return ProxyResponse(
            text='URL does not actually resolve, verify that its correct',
            request_url=url,
            json_response=None
        )
    try:
        json = response.json()
    except JSONDecodeError:
        json = None
    return ProxyResponse(
        text=response.text,
        request_url=response.request.url,
        json_response=json
    )
