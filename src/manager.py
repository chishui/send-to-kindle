#!/usr/bin/env python3

import os
from .book import Book
from .toc import TOC

class Manager(object):
    def __init__(self, book, toc, template):
        self.book = book
        self.toc = toc
        self.template = template

    def make_opf(self):
        opf_template = os.path.join(os.path.join('templates', self.template), 'index.opf');
        with open(opf_template, 'r') as f:
            content = f.read()
            htmls = ''
            order = 1
            if self.toc and self.toc.toc_html:
                htmls = htmls + '<item id="item%d" media-type="application/xhtml+xml" href="%s"></item>\n' \
                        % (order, self.toc.toc_html)
                order = order + 1
            for article in self.book.articles:
                htmls = htmls + '<item id="item%d" media-type="application/xhtml+xml" href="%s"></item>\n' \
                        % (order, article.local_path)
                order = order + 1
            content = content.replace('{htmls}', htmls)

            images = ''
            order = 1
            for article in self.book.articles:
                if not article.local_image: continue
                ext = article.local_image.split('.')[-1]
                images = images +'<item id="image%d" media-type="image/%s" href="%s"/>\n' \
                        % (order, ext, article.local_image)
                order = order + 1
            content = content.replace('{images}', images)

            if self.toc.ncx:
                data = '<item id="My_Table_of_Contents" media-type="application/x-dtbncx+xml" href="%s"/>\n' \
                        % self.toc.ncx
                content = content.replace('{ncx}', data)

            with open('index.opf', 'w') as fout:
                fout.write(content)


if __name__ == '__main__':
    url = 'https://www.nytimes.com/2017/09/19/books/review/ellen-pao-reset-silicon-valley-memoir.html?rref=collection%2Fsectioncollection%2Fbook-review&action=click&contentCollection=review&region=rank&module=package&version=highlights&contentPlacement=11&pgtype=sectionfront'
    book = Book('basic')
    book.add_article(url)
    toc = TOC(book, 'basic')
    toc.make_toc_html()
    toc.make_ncx()
    manager = Manager(book, toc, 'basic')
    manager.make_opf()
