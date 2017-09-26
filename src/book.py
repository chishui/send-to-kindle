#!/usr/bin/env python3

import os
from bs4 import BeautifulSoup
from .article import Article

class Book(object):
    def __init__(self, template):
        self.urls = []
        self.articles = []
        self.template = template

    def add_article(self, url):
        self.urls.append(url)
        article = Article(url)
        article.apply_template('basic')
        self.articles.append(article)


if __name__ == '__main__':
    url = 'https://www.nytimes.com/2017/09/19/books/review/ellen-pao-reset-silicon-valley-memoir.html?rref=collection%2Fsectioncollection%2Fbook-review&action=click&contentCollection=review&region=rank&module=package&version=highlights&contentPlacement=11&pgtype=sectionfront'
    book = Book('basic')
    book.add_article(url)
