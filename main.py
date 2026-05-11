from fastapi import FastAPI

from routes.url_router import router as url_router
from routes.user_router import router as user_router
from routes.auth import router as login_router

app = FastAPI()

app.include_router(url_router)
app.include_router(user_router)
app.include_router(login_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}

