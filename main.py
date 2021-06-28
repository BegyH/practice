from typing import Optional
from fastapi import FastAPI
from colorthief import ColorThief
import aiohttp
from starlette.responses import HTMLResponse
import uvicorn 
import asyncio
import time
import io

from aiohttp import ClientSession

app = FastAPI()

# @asyncio.coroutine
async def load_image(url: str, session: ClientSession):
    print(f"Загружаю {url}")
    image_request = await session.request(method='GET', url=url)
    simple = image_request.content.read_nowait()
    not_simple = io.BytesIO(simple)

    color_thief = ColorThief(not_simple)
    return color_thief.get_color(quality = 1)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    async with ClientSession() as session:
        t1 = time.time()
        r = await session.request(method='GET', url='https://jsonplaceholder.typicode.com/photos')
        r = await r.json()
        tasks = [load_image(img["thumbnailUrl"], session) for img in r[:100]]
        d = await asyncio.gather(*tasks)
    print('Time' , time.time() - t1)
    return  f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Костя красавчик</h1>""" + "".join(  [f"<div style=\"background:rgb({','.join([str(a) for a in i])})\">hui</div>" for i in d]) +"""</body>
</html>"""

# 4.11 4.24 3.83 
# 0.9  1.0
# 4.93 5.44
# 101.17463517189026 
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# Чтобы запустить программу испоолните poetry run python main.py
if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, log_level="info", reload=True)
else:
    a = 1
