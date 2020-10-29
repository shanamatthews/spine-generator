import requests
import xmltodict
from dotenv import load_dotenv
import os

from typing import Final

load_dotenv()

API_KEY = os.getenv("KEY")
API_VERSION: Final = 2
USER_ID: Final = '59980712'
GR_SHELF: Final = 'read'

params = {'v': API_VERSION, 'id': USER_ID, 'shelf': GR_SHELF, 'key':API_KEY}
response = requests.get('https://www.goodreads.com/review/list', params=params)
print(response.url)

reviews = xmltodict.parse(response.content)


reviews = reviews['GoodreadsResponse']['reviews']['review']
print(reviews[1]['book']['title_without_series'])
print(reviews[1]['book']['image_url'])

