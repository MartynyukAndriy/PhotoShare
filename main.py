import uvicorn
from fastapi import FastAPI

from src.repository import comments

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}


app.include_router(comments.router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)