import uvicorn
from fastapi import FastAPI

from src.routes import images

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}


app.include_router(images.router, prefix='/api')
