import requests
import xmltodict
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("KEY")

params = {'v': '2', 'id': '59980712', 'shelf': 'read', 'key':api_key}
response = requests.get('https://www.goodreads.com/review/list', params=params)
reviews = xmltodict.parse(response.content)

reviews = reviews['GoodreadsResponse']['reviews']['review']
print(reviews[0])
