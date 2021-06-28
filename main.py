from typing import Optional
from fastapi import FastAPI
import requests
import uvicorn 


app = FastAPI()


@app.get("/")
def read_root():
    r = requests.get('https://jsonplaceholder.typicode.com/photos')
    r = r.json()
    return r


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# Чтобы запустить программу испоолните poetry run python main.py
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")