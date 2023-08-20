from fastapi import FastAPI
import uvicorn
from pymongo import MongoClient

import redis
import time

rd = redis.Redis(host="host.docker.internal", port=6379, db=0)

app = FastAPI()


@app.get('/cache')
async def get_items_2():
    cache = rd.get("time")
    if cache:
        cache
    else:
        rd.set("time", str(time.time()))
        rd.expire("time", 180)
        return str(time.time())
    



@app.get('/')
async def get_items(limit: int = 10):
    cache = rd.get(limit)
    if cache:
        print("cache result")
        return json.loads(cache)
    else:
        client = MongoClient('mongodb://root:example@host.docker.internal', 27017)
    
        # Database Name
        db = client["local"]
        
        # Collection Name
        col = db["assets"]
        result = list(col.find().limit(limit))
        rd.set(limit, result)
        rd.expire(limit, 180)
        return {"time":str(time.time()),"data":str(result)}