import unittest
import credentials
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': credentials.API_KEY,
}


class test_usd_ingestion(unittest.TestCase):

    def test_origin_is_up(self):
        session = Session()
        session.headers.update(headers)
        response = session.get(url)
        self.assertIsNotNone(response)

    def test_url_status_OK(self):
        session = Session()
        session.headers.update(headers)
        response = session.get(url)
        self.assertIsNotNone(response)
        self.assertEquals(response.status_code, 200)

    def test_url_status_KO(self):
        session = Session()
        response = session.get(url)
        self.assertIsNotNone(response)
        self.assertEquals(response.status_code, 401)
    def test_format_expected(self):
        session = Session()
        session.headers.update(headers)
        response = session.get(url)
        self.assertIsNotNone(response)
        self.assertEquals(response.status_code, 200)
        data=json.loads(response.text)
        self.assertIsNotNone(data.get('data'))
        self.assertGreater(len(data.get('data')),0)
        self.assertIsNotNone(data.get('data')[0].get("quote").get("USD").get("price"))            

if __name__ == '__main__':
    unittest.main()
