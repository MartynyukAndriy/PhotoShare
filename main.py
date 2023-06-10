import uvicorn
from fastapi import FastAPI

from src.routes import transformed_picture, auth, tags, comments_routes

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}


app.include_router(comments_routes.router, prefix='/api')
app.include_router(transformed_picture.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(tags.router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
