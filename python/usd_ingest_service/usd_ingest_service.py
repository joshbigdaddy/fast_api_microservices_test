from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pymongo import MongoClient
import credentials

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
  print(len(data))
  print(data.get("status"))
  print(data.get("data"))

  db = client['local']
  collection_status = db['status']
  collection_usd = db['USD_values']
  # if pymongo >= 3.0 use insert_many() for inserting many documents
  collection_status.insert_one(data.get("status"))
  collection_usd.insert_many(data.get("data"))


  client.close()
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

