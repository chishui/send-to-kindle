#!/usr/bin/env python3

import os
from .book import Book

class TOC(object):
    def __init__(self, book, template):
        self.book = book
        self.template = template
        self.toc_html = None
        self.ncx = None

    def make_toc_html(self):
        toc_template = os.path.join(os.path.join('templates', self.template), 'toc.html');
        with open(toc_template, 'r') as f:
            content = ''
            # add title
            content = content + '<h1><b>%s</b></h1>\n' % 'TABLE OF CONTENTS'
            # add chapters
            for article in self.book.articles:
                chapter = '<h3><b><a href="%s">%s</a></b></h3>\n' % (article.local_path, article.title)
                content = content + chapter

            html = f.read()
            html = html.replace('{items}', content)
            output = 'toc.html'
            with open(output, 'w') as fout:
                fout.write(html)
                self.toc_html = output

    def add_toc_to_ncx(self):
        if not self.toc_html:
            return (None, 1)

        item = '''
    <navPoint class="toc" id="toc" playOrder="1">
      <navLabel>
        <text>Table of Contents</text>
      </navLabel>
      <content src="%s"/>
    </navPoint>
        ''' % self.toc_html
        return (item, 2)

    def make_ncx(self):
        items = ''
        ncx_template = os.path.join(os.path.join('templates', self.template), 'index.ncx');
        item, order = self.add_toc_to_ncx()
        if item:
            items = items + item

        for article in self.book.articles:
            item = '''
    <navPoint class="article" id="article_%d" playOrder="%d">
      <navLabel>
        <text>%s</text>
      </navLabel>
      <content src="%s"/>
    </navPoint>
            ''' % (order, order, article.title, article.local_path)
            items = items + item

        with open(ncx_template, 'r') as f:
            content = f.read()
            content = content.replace('{items}', items)

            self.ncx = 'index.ncx'
            with open('index.ncx', 'w') as fout:
                fout.write(content)


if __name__ == '__main__':
    url = 'https://www.nytimes.com/2017/09/19/books/review/ellen-pao-reset-silicon-valley-memoir.html?rref=collection%2Fsectioncollection%2Fbook-review&action=click&contentCollection=review&region=rank&module=package&version=highlights&contentPlacement=11&pgtype=sectionfront'
    book = Book('basic')
    book.add_article(url)
    toc = TOC(book, 'basic')
    toc.make_ncx()




