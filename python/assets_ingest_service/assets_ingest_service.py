from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pymongo import MongoClient

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
  #print(data)
  client = MongoClient('mongodb://root:example@host.docker.internal', 27017)
  print(len(data))
  db = client['local']
  #collection_status = db['status']
  collection_assets = db['assets']
  #collection_status.insert_one(data.get("status"))
  collection_assets.insert_many(convert_numeric_to_str(data.get("Data")))


  client.close()
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

