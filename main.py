import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)