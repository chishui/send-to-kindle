#!/usr/bin/env python3

import os
from bs4 import BeautifulSoup
import urllib
from newspaper import Article as NewsArticle

cur_path = os.getcwd()
template_path = os.path.join(cur_path, 'templates')

class Article(NewsArticle):
    def __init__(self, *args, **kwargs):
        NewsArticle.__init__(self,*args, **kwargs)
        self.download()
        self.parse()
        self.local_image = None
        self.download_image('img')

    def download_image(self, path) :
        url = self.top_image
        if not url: return False

        if not os.path.exists(path) :
            os.mkdir(path)

        file = url.split('/')[-1]
        response = urllib.request.urlopen(url)
        with open(os.path.join(os.path.join(cur_path, path), file), 'wb') as f:
            f.write(response.read())
            self.local_image = os.path.join(path, file)

    def apply_template(self, template):
        path = os.path.join(os.path.join(template_path, template), 'index.html')
        with open (path, 'r') as f:
            html = f.read()
            title = '<h1>%s</h1>' % self.title
            html = html.replace('{title}', title)

            if self.local_image:
                img = '<img src="%s" />' % self.local_image
                html = html.replace('{top_image}', img)

            content = '<pre>%s</pre>' % self.text
            html = html.replace('{content}', content)

            link = '<a href="%s">%s</a>' % (self.url, self.url)
            html = html.replace('{link}', link)

            with open(self.title + '.html', 'w') as fout:
                fout.write(html)
                self.local_path = self.title + '.html'

if __name__ == '__main__':
    url = 'https://www.nytimes.com/2017/09/19/books/review/ellen-pao-reset-silicon-valley-memoir.html?rref=collection%2Fsectioncollection%2Fbook-review&action=click&contentCollection=review&region=rank&module=package&version=highlights&contentPlacement=11&pgtype=sectionfront'
    article = Article(url)
    article.apply_template('basic')
