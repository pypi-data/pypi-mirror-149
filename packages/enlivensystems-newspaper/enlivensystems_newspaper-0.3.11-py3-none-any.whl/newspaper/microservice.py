from fastapi import FastAPI
from newspaper import extract
from newspaper.api import Request

app = FastAPI()

@app.post('/hu')
async def handle(request: Request):
    return extract(request, 'hu')

@app.post('/en')
async def handle(request: Request):
    return extract(request, 'en')