import uvicorn
from fastapi import FastAPI
from src.routes import auth

from src.routes import transformed_picture

from src.repository import comments

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}


app.include_router(comments.router, prefix='/api')
app.include_router(transformed_picture.router, prefix='/api')
app.include_router(auth.router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
