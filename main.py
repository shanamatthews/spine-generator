import requests
import xmltodict
from dotenv import load_dotenv
import os
import csv

from typing import Final

load_dotenv()

API_KEY = os.getenv("KEY")
API_VERSION: Final = 2
USER_ID: Final = '59980712'
GR_READ_SHELF: Final = 'read'
GR_READING_SHELF: Final = 'currently-reading'

NUM_BOOKS: Final = 60

def main():
    read_params = {'v': API_VERSION, 'id': USER_ID, 'shelf': GR_READ_SHELF, 'key': API_KEY, 'sort': 'date_read', 'per_page': NUM_BOOKS}
    read_response = requests.get('https://www.goodreads.com/review/list', params=read_params)

    reading_params = {'v': API_VERSION, 'id': USER_ID, 'shelf': GR_READING_SHELF, 'key': API_KEY, 'sort': 'date_read'}
    reading_response = requests.get('https://www.goodreads.com/review/list', params=reading_params)

    books_read = xmltodict.parse(read_response.content)['GoodreadsResponse']['reviews']['review']
    books_reading = xmltodict.parse(reading_response.content)['GoodreadsResponse']['reviews']['review']

    # print(books_read[16])

    create_book_csv(books_read, 'recently-read.csv')
    create_book_csv(books_reading, 'currently-reading.csv', currently_reading=True)

def create_book_csv(book_array, file_name, currently_reading=False):
    with open(file_name, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        headers = ['Title', 'Date', 'NumPages', 'ImageURL']

        filewriter.writerow(headers)

        for book in book_array:
            date = ""
            if currently_reading:
                date = book['started_at']
            else:
                date = book['read_at'] if book['read_at'] != None else book['date_updated']

            book_data = book['book']
            filewriter.writerow([book_data['title_without_series'], date, book_data['num_pages'], book_data['image_url']])

if __name__ == "__main__":
    main()
