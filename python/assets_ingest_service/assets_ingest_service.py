from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pymongo import MongoClient
import multiprocessing
import time

cpu_count = multiprocessing.cpu_count()
client = MongoClient('mongodb://root:example@host.docker.internal', 27017,maxPoolSize=cpu_count+1)

def convert_numeric_to_str(d):
    cur_type = type(d)

    if cur_type == dict:
        for key, value in d.items():
            d[key] = convert_numeric_to_str(value)

    elif cur_type == list:
        for i, el in enumerate(d):
            d[i] = convert_numeric_to_str(el)

    else:
        if cur_type in [int, float]:
            d = str(d)

    return d

def convert_str_to_numeric(d):
    cur_type = type(d)

    if cur_type == dict:
        for key, value in d.items():
            d[key] = convert_str_to_numeric(value)

    elif cur_type == list:
        for i, el in enumerate(d):
            d[i] = convert_str_to_numeric(el)

    else:
        if cur_type == str:
            try:
                d = int(d)
            except ValueError:
                try:
                    d = float(d)
                except ValueError:
                    pass

    return d

def insert_chunk(chunk):
    db = client['local']
    collection_assets = db['assets']
    if len(chunk)>1:
        collection_assets.insert_one(convert_numeric_to_str(chunk))
if __name__ == '__main__':
    url = 'https://min-api.cryptocompare.com/data/top/totaltoptiervolfull'
    parameters = {
    'tsym':'USD',
    'limit':'100'
    }
    headers = {
    'Accepts': 'application/json'
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url,params=parameters)
        data = json.loads(response.text)
        total_documents_count = len(data.get("Data"));
        assets = data.get("Data")
        db = client['local']
        #collection_status = db['status']
        collection_assets = db['assets']
        #TRUNCATE PREVIOUS DATA
        collection_assets.delete_many({})
        pool = multiprocessing.Pool(processes=cpu_count)
        documents_number = int(total_documents_count/cpu_count)
        #a=time.time()
        result = pool.map(insert_chunk,assets,chunksize=documents_number)   #creates chunks of total_documents_count/cpu_count  pool.close()
        #print(time.time()-a)
        client.close()
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

