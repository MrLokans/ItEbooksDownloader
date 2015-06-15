#!/usr/bin/env python
import os
import json
import requests

from bs4 import BeautifulSoup as bs

BASIC_URL = "http://it-ebooks.info/book/"
DOWNLOAD_DIR = "IT_BOOKS"


class Book(object):

    def __init__(self, bs_object):
        self.__soup = bs_object
        self.title = self.get_title()
        self.subtitle = self.get_subtitle()
        self.description = self.get_description()
        self.author = ""
        self.ISBN = ""
        self.year = ""
        self.pages = ""
        self.format = ""
        self.download_url = ""
        self.cover_url = ""

    def get_authors(self):
        pass

    def get_title(self):
        try:
            return self.__soup.h1.text
        except AttributeError:
            print("No title found for the book.")
            return ""

    def get_subtitle(self):
        try:
            return self.__soup.h3.text
        except AttributeError:
            print("No subtitle found for the book.")
            return ""

    def get_description(self):
        return self.__soup.find("span", itemprop="description").text

    def get_year(self):
        return self.__soup.find("b", itemprop="datePublished").text

    def get_pages(self):
        return self.__soup.find("b", itemprop="numberOfPages").text

    def get_format(self):
        return self.__soup.find("b", itemprop="bookFormat").text

    def get_url(self):
        return self.__soup.find("b", itemprop="author").text

    def get_isbn(self):
        return self.__soup.find("b", itemprop="isbn").text

    def write_metadata(self):
        pass

    def download_book(self):
        pass

    def to_json(self):
        pass

    def __repr__(self):
        return "<Book '{} - {}'>".format(self.title, self.subtitle)


def main():
    if not os.path.exists(DOWNLOAD_DIR):
        os.mkdir(DOWNLOAD_DIR)
    book_num = 5786
    for i in range(1, book_num+1):
        book_url = "".join([BASIC_URL, str(i)])
        print("Analyzing {url}".format(url=book_url))
        r = requests.get(book_url)
        soup = bs(r.text)
        book = Book(soup)

        print("Title: ", book.title)
        print("Subtitle:", book.subtitle)
        print("Description: ", book.description)
        print("-=" * 10)
        if i > 30:
            exit(0)


def get_book_number():
    pass


def save_book_description():
    pass


def save_book_cover():
    pass


def download_book(download_url):
    pass

if __name__ == '__main__':
    main()