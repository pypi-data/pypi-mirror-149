"""The module provides implementation for converting RSS contents to several formats"""

import logging
import os
from typing import List

from xhtml2pdf import pisa
from yattag import Doc, indent

logger = logging.getLogger()


class Converter:
    """Represents rss-to-file converter"""

    def __init__(self, rss_contents: List[tuple]) -> None:
        """Converter constructor

        Args:
            rss_contents: List containing the news items
        """
        self._rss_contents = rss_contents
        self._html_content = None

    def _to_html(self) -> None:
        """Converts news items to HTML

        Returns:
            None
        """
        doc, tag, text = Doc().tagtext()
        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            doc.stag('meta', charset='utf-8')
            with tag('body'):
                doc.attr(style="text-align:left; font-size:20px")
                for item in self._rss_contents:
                    with tag('h1'):
                        text(f"Title: {item[2]}")
                    with tag('h3'):
                        text(f"Date published: {item[3]}")
                    with tag('h4'):
                        text(f"Feed source: {item[1]}")
                    with tag('div'):
                        doc.attr(style="word-wrap: break-word; width: 1000px; line-height:25px")
                        text(f"{item[4]}\n")
                    with tag('a'):
                        doc.attr(href=f"{item[5]}")
                        doc.stag('br')
                        text('Read more here')
                        doc.stag('br')
                        doc.stag('br')
                    with tag('div'):
                        if item[6] != 'No Image':
                            doc.stag('img', src=f"{item[6]}")
                            doc.attr(style="zoom:100%")
                        else:
                            text('Image is not available')
        self._html_content = indent(doc.getvalue())

    def generate_file(self, filetype: str, filepath: str) -> None:
        """Generates HTML/PDF file

        Returns:
            None
        """
        self._to_html()
        file_ = os.path.join(filepath, f'news.{filetype}')
        os.makedirs(os.path.dirname(file_), exist_ok=True)
        if filetype == 'pdf':
            with open(file_, 'w+b') as file:
                print('Creating PDF file...')
                logging.disable(logging.DEBUG)
                pisa.CreatePDF(self._html_content, dest=file)
                print(f'PDF file created at {os.path.abspath(file_)}')
        elif filetype == 'html':
            with open(file_, 'w') as file:
                print('Creating HTML file...')
                file.write(self._html_content)
                print(f'HTML file created at {os.path.abspath(file_)}')
