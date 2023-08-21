from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pymongo import MongoClient
import multiprocessing
import time
import credentials

cpu_count = multiprocessing.cpu_count()
client = MongoClient('mongodb://root:example@host.docker.internal', 27017,maxPoolSize=cpu_count+1)
def insert_chunk(chunk):
    db = client['local']
    collection_assets = db['USD_values']
    if len(chunk)>1:
        collection_assets.insert_one(chunk)

if __name__ == '__main__':

  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
  parameters = {
    'convert':'USD'
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': credentials.API_KEY,
  }

  session = Session()
  session.headers.update(headers)

  try:
    response = session.get(url)
    data = json.loads(response.text)
    client = MongoClient('mongodb://root:example@host.docker.internal', 27017)

    db = client['local']
    collection_status = db['status']
    collection_usd = db['USD_values']
    #TRUNCATE PREVIOUS DATA
    collection_status.delete_many({})
    collection_usd.delete_many({})
    #TRUNCATE PREVIOUS DATA
    usd = data.get("data")
    total_documents_count = len(usd);
    pool = multiprocessing.Pool(processes=cpu_count)
    documents_number = int(total_documents_count/cpu_count)
    collection_status.insert_one(data.get("status"))
    #a=time.time()
    result = pool.map(insert_chunk,usd,chunksize=documents_number)   #creates chunks of total_documents_count/cpu_count  pool.close()
    #print(time.time()-a)

    client.close()
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

