from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

base_url = 'https://jsonplaceholder.typicode.com/todos'

async def request_base(number):
    async with httpx.AsyncClient() as client:
        return await client.get(f"{base_url}/{number}")

@app.get("/todo/{number}")
async def get_todo(number):
    responce = await request_base(number)

    # This is weird, but without dropping this header response isn't correct
    # And can't be opened with browser or printed with curl
    # Probably, base_url server does something wrong
    responce.headers.pop('content-encoding')

    return JSONResponse(content=responce.json(), headers=responce.headers, status_code=responce.status_code)