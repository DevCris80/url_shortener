from fastapi import FastAPI

from routes.shortener import router as url_router

app = FastAPI()

app.include_router(url_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

