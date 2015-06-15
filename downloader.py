#!/usr/bin/env python
import os
import json
import requests

from collections import OrderedDict
from bs4 import BeautifulSoup as bs

BASE_URL = "http://it-ebooks.info"
BASIC_URL = "http://it-ebooks.info/book/"
DOWNLOAD_DIR = "IT_BOOKS"


class Book(object):

    def __init__(self, bs_object):
        self.__soup = bs_object
        self.__site_table = self.__soup.find(class_="ebook_view")
        self.title = self.get_title()
        self.subtitle = self.get_subtitle()
        self.description = self.get_description()
        self.authors = self.get_authors()
        self.ISBN = self.get_isbn()
        self.year = self.get_year()
        self.pages = self.get_pages()
        self.format = self.get_format()
        self.download_url = self.get_url()
        self.cover_url = self.get_cover_url()

    def get_authors(self):
        return ""

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
        return self._tag_info("span", {"itemprop": "description"})

    def get_year(self):
        return self._tag_info("b", {"itemprop": "datePublished"})

    def get_pages(self):
        return self._tag_info("b", {"itemprop": "numberOfPages"})

    def get_format(self):
        return self._tag_info("b", {"itemprop": "bookFormat"})

    def get_isbn(self):
        return self._tag_info("b", {"itemprop": "isbn"})

    def get_url(self):
        # TODO: completely rethink this idea of obtaining url
        return self.__site_table.tr.findAll("td")[21].a["href"]

    def get_cover_url(self):
        return "".join([BASE_URL, self.__site_table.find("img", itemprop="image")["src"]])

    def write_metadata(self):
        pass

    def download_book(self):
        pass

    def to_json(self):
        json_meta = OrderedDict()
        json_meta.update({
                    "title": self.title,
                    "subtitle": self.subtitle,
                    "authors": self.authors,
                    "description": self.description,
                    "url": self.download_url,
                    "cover_url": self.cover_url,
                    "isbn": self.ISBN,
                    "format": self.format,
                    "pages": self.pages
        })
        return json.dumps(json_meta)

    def _tag_info(self, tag_name, attr_dict):
        try:
            return self.__site_table.find(tag_name, **attr_dict).text
        except AttributeError:
            return ""

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
        print("Author: ", book.authors)
        print("Pages: ", book.pages)
        print("Year: ", book.year)
        print("Cover url: ", book.cover_url)
        print("Book url: ", book.download_url)
        print("JSON: ", book.to_json())
        # r = requests.get(book.download_url)
        print("-=" * 10)
        if i > 3:
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
