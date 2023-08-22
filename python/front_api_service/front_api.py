from fastapi import FastAPI
import uvicorn
from pymongo import MongoClient

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
import time
import multiprocessing
import time
import json
import bson

app = FastAPI()
cpu_count = multiprocessing.cpu_count()
client = MongoClient('mongodb://root:example@host.docker.internal', 27017,maxPoolSize=cpu_count+1)

def create_register(chunk):
    db = client['local']
    collection_usd = db['USD_values']
    id=chunk.get("CoinInfo").get("Name")
    usd=collection_usd.find({"symbol":id},{"quote":1})
    usd=list(usd)
    if(len(usd)>0):
        price = usd[0].get("quote").get("USD").get("price")
    else:
        price = 0.0
    
    res= {"Rank":chunk.get("rank"),"symbol":id, "Price USD":price}
    return res


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
 
    # Database Name
    db = client["local"]
    
    # Collection Name
    col = db["assets"]
    assets = list(col.find().sort("rank").limit(limit))
    pool = multiprocessing.Pool(processes=cpu_count)
    documents_number = int(limit/cpu_count)
    a=time.time()
    result = pool.map(create_register,assets,chunksize=documents_number)   #creates chunks of total_documents_count/cpu_count  pool.close()
    print(time.time()-a)
    return json.dumps(result)

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://host.docker.internal", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#http://localhost/docs to see the swagger API