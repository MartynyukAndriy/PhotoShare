import uvicorn
from fastapi import FastAPI
from src.routes import auth

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}


app.include_router(auth.router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
