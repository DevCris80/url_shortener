from fastapi import FastAPI

from routes.shortener import router as url_router
from routes.user import router as user_router

app = FastAPI()

app.include_router(url_router)
app.include_router(user_router, prefix="/user", tags=["user"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

