"""The module provides implementation to aggregate RSS content"""

import sys
from logging import getLogger
from typing import Optional, List

import requests
from bs4 import BeautifulSoup

from db_manager.manager import DatabaseManager

logger = getLogger()


class RSSAggregator:
    """Represents RSS content aggregation"""

    def __init__(self, url: str, content_pub_date: Optional[str] = None, content_limit: Optional[int] = None) -> None:
        """RSSContent constructor

        Args:
            url: Limit of the feeds
            content_pub_date: News publishing date
            content_limit: URL of RSS feed

        Returns:
            None
        """
        self.url = url
        self._content_pub_date = content_pub_date
        self._content_limit = content_limit
        self._parsed_rss_content = []
        self._response_object = None

    def _fetch_rss_content(self) -> None:
        """Fetches RSS page based on URL

        Returns:
            None
        """
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        logger.debug(f'Making HTTP request to {self.url}')
        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            logger.error(f'Ambiguous exception while making request to {self.url}')
            sys.exit('Error occurred while making request. Program terminated. Try again.')
        self._response_object = response
        logger.debug('Response arrived.')

    def _parse_rss_content(self) -> None:
        """Parses the XML contents of the Response object

        Returns:
            None
        """
        logger.debug('Parsing fetched content...')
        soup = BeautifulSoup(self._response_object.text, 'xml')
        articles = soup.find_all('item', limit=self._content_limit)

        for article in articles:
            news_item = {
                'feed_url': self.url,
                'feed_title': soup.channel.title.text,
                'article_title': article.title.text,
                'publication_date': article.pubDate.text if article.pubDate else 'No Publication Date',
                'description': article.description.text if article.description else 'No Description',
                'link': article.link.text,
                'image_link': article.find(attrs={'medium': 'image'})['url'] if article.find(
                    attrs={'medium': 'image'}) else 'No Image',
            }
            self._parsed_rss_content.append(news_item)
        logger.debug('Parsing complete.')

    def _aggregate_content(self) -> List[tuple]:
        """Aggregates data

        Returns:
            List of fetched rows
        """
        if self.url != '' and self._content_pub_date is None:
            self._fetch_rss_content()
            self._parse_rss_content()
        db = DatabaseManager(table_name='news',
                             table_cols=['feed_url', 'feed_title', 'article_title', 'publication_date', 'description',
                                         'link',
                                         'image_link'],
                             unique_constraint='link')
        db.insert_into_table(self._parsed_rss_content)
        fetched_rows = db.retrieve_from_db(self._content_pub_date, self.url, self._content_limit)
        if len(fetched_rows) == 0:
            logger.error('Records not available for the date specified')
            sys.exit('No records. Program terminated. Try again.')
        return fetched_rows

    def retrieve_from_storage(self) -> List[tuple]:
        """Retrieves SQL query result

        Returns:
            List of fetched rows
        """
        return self._aggregate_content()
