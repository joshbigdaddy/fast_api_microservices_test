from fastapi import FastAPI, HTTPException
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
import os

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

def wait_status_ready(db):
    counter=0
    while True:
        status = db["status"]
        status_assets = db["status_assets"]

        status_cursor=status.find()
        status_assets_cursor=status_assets.find()

        if len(list(status_cursor)) or len(list(status_assets_cursor))==0:
            time.sleep(5)
        else:
            break
        counter+=1
        if counter >= 6:
            raise HTTPException(status_code=408, detail="Timeout due to data not present in origin")

@cache()
async def get_cache():
    return 1

@app.get('/cache')
@cache(expire=60)
async def get_cache():
    return str(time.time())

@app.get('/')
@cache(expire=60)
async def get_items(limit: int = 10):
    if limit <= 0:
        #we raise a Unprocessable Entity CODE which means that the get is OK but the args are not
        raise HTTPException(status_code=422, detail="Limit value has a default of 10 and it must be higher than 0")
    # Database Name
    db = client["local"]
    
    # Collection Name
    col = db["assets"]
    #We check if status dbs are ready and we wait 5 seconds for them to be ready. this grants us with a bit of time to answer requests while data is being regenerated
    if not bool(os.getenv("TEST_RUNNING", "False")):
        wait_status_ready(db)

    assets = list(col.find().sort("rank").limit(limit))
    pool = multiprocessing.Pool(processes=cpu_count)
    documents_number = max(int(limit/cpu_count),1)
    #a=time.time()
    result = pool.map(create_register,assets,chunksize=documents_number)   #creates chunks of total_documents_count/cpu_count  pool.close()
    #print(time.time()-a)
    return {"last_status_information":list(db["status"].find())[0].get("timestamp"),"data": result}

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://host.docker.internal", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#http://localhost/docs to see the swagger API