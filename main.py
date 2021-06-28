from typing import Optional
from fastapi import FastAPI
from colorthief import ColorThief
import requests
import uvicorn 


app = FastAPI()


@app.get("/")
def read_root():
    r = requests.get('https://jsonplaceholder.typicode.com/photos')
    r = r.json()
    d = []
    for i in r[:5]:
        image_request = requests.get(i["thumbnailUrl"], stream = True)
        simple = image_request.raw
        simple.decode_content = True
        color_thief = ColorThief(simple)
        d.append(color_thief.get_color(quality = 1))
    return d


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# Чтобы запустить программу испоолните poetry run python main.py
if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, log_level="info", reload=True)
else:
    a = 1
