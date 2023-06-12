
import uvicorn
from fastapi import FastAPI
from src.routes import tags, ratings

app = FastAPI()

app.include_router(ratings.router, prefix='/api')

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)