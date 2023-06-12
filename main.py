import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from src.conf.config import settings
from src.routes import transformed_images, auth, tags, comments_routes, images, ratings

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
    await FastAPILimiter.init(r)


app.include_router(comments_routes.router, prefix='/api')
app.include_router(transformed_images.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
app.include_router(images.router, prefix='/api')
app.include_router(ratings.router, prefix='/api')



if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
