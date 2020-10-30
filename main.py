import requests
import xmltodict
from dotenv import load_dotenv
import os
import csv
import json
from BookData import BookData

from typing import Final

load_dotenv()

GOODREADS_KEY = os.getenv('GOODREADS_KEY')
API_VERSION: Final = 2
USER_ID: Final = '59980712'
GR_READ_SHELF: Final = 'read'
GR_READING_SHELF: Final = 'currently-reading'

COMPUTER_VISION_KEY = os.getenv('COMPUTER_VISION_KEY')
COMPUTER_VISION_ENDPOINT = os.getenv('COMPUTER_VISION_ENDPOINT')

NUM_BOOKS: Final = 60

def main():

    read_response = get_goodreads_data(currently_reading=False)
    reading_response = get_goodreads_data(currently_reading=True)

    books_read_xml = xmltodict.parse(read_response.content)['GoodreadsResponse']['reviews']['review']
    books_reading_xml = xmltodict.parse(reading_response.content)['GoodreadsResponse']['reviews']['review']

    # print(books_read[16])

    books_read = []
    books_reading = []

    for book_xml in books_read_xml:
        books_read.append(
            BookData(book_xml,
            date=book_xml['read_at'] if book_xml['read_at'] != None else book_xml['date_updated']))

    for book_xml in books_reading_xml:
        books_reading.append(BookData(book_xml, date=book_xml['started_at']))

    # get_image_colors()

    create_book_csv(books_read, 'recently-read.csv')
    create_book_csv(books_reading, 'currently-reading.csv')


def get_image_colors(image_ur):
    analyze_url = COMPUTER_VISION_ENDPOINT + 'vision/v3.1/analyze'
    headers = {'Ocp-Apim-Subscription-Key': COMPUTER_VISION_KEY}
    params = {'visualFeatures': 'Categories,Description,Color'}
    data = {'url': analyze_url}
    response = requests.post(analyze_url, headers=headers,
                         params=params, json=data)

    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    print(json.dumps(response.json()))
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()

def get_goodreads_data(currently_reading=False):
    shelf = GR_READ_SHELF
    if currently_reading:
        shelf = GR_READING_SHELF

    params = {'v': API_VERSION, 'id': USER_ID, 'shelf': shelf, 'key': GOODREADS_KEY, 'sort': 'date_read'}
    response = requests.get('https://www.goodreads.com/review/list', params=params)

    return response

def create_book_csv(book_array, file_name):
    with open(file_name, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        headers = ['Title', 'Date', 'NumPages', 'ImageURL']
        filewriter.writerow(headers)

        for book in book_array:
            filewriter.writerow([book.title, book.date, book.numPages, book.imageUrl])

if __name__ == "__main__":
    main()
