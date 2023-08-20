from fastapi import FastAPI
import uvicorn
from pymongo import MongoClient

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
import time

app = FastAPI()

@cache()
async def get_cache():
    return 1

@app.get('/cache')
@cache(expire=60)
async def get_items_2():
    return str(time.time())



@app.get('/')
@cache(expire=60)
async def get_items(limit: int = 10):
    client = MongoClient('mongodb://root:example@host.docker.internal', 27017)
 
    # Database Name
    db = client["local"]
    
    # Collection Name
    col = db["assets"]
    result = list(col.find().limit(limit))
    return {"time":str(time.time()),"data":str(result)}

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://host.docker.internal", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#http://localhost/docs to see the swagger API