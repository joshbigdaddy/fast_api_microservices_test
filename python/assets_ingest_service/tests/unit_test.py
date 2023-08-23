import unittest
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://min-api.cryptocompare.com/data/top/totaltoptiervolfull'
parameters = {
'tsym':'USD',
'limit':'100'
    }
headers = {
    'Accepts': 'application/json'
}

class test_assets_ingestion(unittest.TestCase):

    def test_origin_is_up(self):
        session = Session()
        session.headers.update(headers)
        response = session.get(url,params=parameters)
        self.assertIsNotNone(response)

    def test_url_status_OK(self):
        session = Session()
        session.headers.update(headers)
        response = session.get(url,params=parameters)
        self.assertIsNotNone(response)
        self.assertEquals(response.status_code, 200)
    
    def test_url_status_KO(self):
        session = Session()
        response = session.get(url)
        self.assertIsNotNone(response)
        self.assertIs(len(json.loads(response.text).get('Data')), 0)
    
    def test_format_expected(self):
        session = Session()
        session.headers.update(headers)
        response = session.get(url,params=parameters)
        self.assertIsNotNone(response)
        self.assertEquals(response.status_code, 200)
        data=json.loads(response.text)
        self.assertIsNotNone(data.get('Data'))
        self.assertGreater(len(data.get('Data')),0)
        self.assertIsNotNone(data.get('Data')[0].get("CoinInfo").get("Name"))            

if __name__ == '__main__':
    unittest.main()
