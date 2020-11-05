import requests
import xmltodict
from dotenv import load_dotenv
import os
import csv
import json
from BookData import BookData

from typing import Final

# get colors from this api instead? http://colormind.io/api-access/

load_dotenv()

GOODREADS_KEY = os.getenv('GOODREADS_KEY')
API_VERSION: Final = 2
USER_ID: Final = '59980712'
GR_READ_SHELF: Final = 'read'
GR_READING_SHELF: Final = 'currently-reading'

COMPUTER_VISION_KEY = os.getenv('COMPUTER_VISION_KEY')
COMPUTER_VISION_ENDPOINT = os.getenv('COMPUTER_VISION_ENDPOINT')

NUM_BOOKS: Final = 20

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

    for book in books_read:
        colors = get_image_colors(book.imageUrl)
        book.coverColor = colors['coverColor']
        book.set_accent_color(colors['accentColor'])

    for book in books_reading:
        colors = get_image_colors(book.imageUrl)
        book.coverColor = colors['coverColor']
        book.set_accent_color(colors['accentColor'])

    create_book_csv(books_read, 'recently-read.csv')
    create_book_csv(books_reading, 'currently-reading.csv')

    # create_book_json(books_read, 'recently-read.json')
    # create_book_json(books_reading, 'currently-reading.json')


def get_image_colors(image_url):
    analyze_url = COMPUTER_VISION_ENDPOINT + 'vision/v3.1/analyze'
    headers = {'Ocp-Apim-Subscription-Key': COMPUTER_VISION_KEY}
    params = {'visualFeatures': 'Categories,Description,Color'}
    data = {'url': image_url}
    response = requests.post(analyze_url, headers=headers,
                         params=params, json=data)

    response.raise_for_status()

    analysis = response.json()

    image_colors = {'coverColor': analysis['color']['dominantColorBackground'], 'accentColor': analysis['color']['accentColor']}
    return image_colors

def get_goodreads_data(currently_reading=False):
    shelf = GR_READ_SHELF
    if currently_reading:
        shelf = GR_READING_SHELF

    params = {'v': API_VERSION, 'id': USER_ID, 'shelf': shelf, 'key': GOODREADS_KEY, 'sort': 'date_read'}
    response = requests.get('https://www.goodreads.com/review/list', params=params)

    return response

# This doesn't jsonify correctly
def create_book_json(book_array, file_name):
    with open(file_name, 'w') as jsonfile:
        for book in book_array:
            json.dump(book.to_json(), jsonfile)

def create_book_csv(book_array, file_name):
    with open(file_name, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        headers = ['Title', 'Date', 'NumPages', 'CoverColor', 'AccentColor', 'ImageURL']
        filewriter.writerow(headers)

        for book in book_array:
            filewriter.writerow([book.title, book.date, book.numPages, book.coverColor, book.accentColor, book.imageUrl])

if __name__ == "__main__":
    main()
