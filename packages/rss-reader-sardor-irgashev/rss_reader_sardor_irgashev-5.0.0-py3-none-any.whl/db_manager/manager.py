"""The module provides implementation for managing database connections"""

import os
import sqlite3
import sys
from datetime import datetime
from logging import getLogger
from typing import List

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
logger = getLogger()


class DatabaseManager:
    """Represents Database management"""

    def __init__(self, table_name: str, table_cols: List[str], unique_constraint: str) -> None:
        """DatabaseManager constructor

        Args:
            table_name: Name of the to be created database table
            table_cols: Column names of the to be created database tables
            unique_constraint: Unique constraint column name

        Returns:
            None
        """
        self._table_name = table_name
        self._table_columns = table_cols
        self._db_connection = sqlite3.connect(os.path.join(ROOT_DIR, f'{table_name}.db'))
        self._cursor = self._db_connection.cursor()
        self._columns = ', '.join(self._table_columns)
        self._placeholders = ':' + ', :'.join(self._table_columns)
        self._unique = unique_constraint
        logger.debug(f'Connected to DB.')

    def _create_table(self) -> None:
        """Creates table in database

        Returns:
            None
        """
        query = f"CREATE TABLE IF NOT EXISTS {self._table_name} ({self._columns}, unique ({self._unique}))"
        self._cursor.execute(query)
        logger.debug(f'Table {self._table_name} operating.')

    def insert_into_table(self, content: List[dict]) -> None:
        """Inserts rows into database

        Args:
            content: List of dictionaries containing to be inserted data

        Returns:
            None
        """
        self._create_table()
        query = f"INSERT OR IGNORE INTO {self._table_name} ({self._columns}) VALUES ({self._placeholders})"
        self._cursor.executemany(query, content)
        self._db_connection.commit()

    def _query_db(self, date: str, source: str) -> None:
        """Performs SELECT queries on database

        Args:
            date: News publishing date
            source: Feed source

        Returns:
            None
        """
        if date is not None:
            pub_date = datetime.strptime(date, '%Y%m%d').strftime('%a, %d %b %Y') + '%'
            if source != '':
                query = f"""
                SELECT * FROM {self._table_name} WHERE feed_url=:source and publication_date like :publication_date"""
                self._cursor.execute(query, {'publication_date': pub_date, 'source': source})
                logger.debug('Query performed to fetch rows according to source and publishing date.')
            else:
                query = f"SELECT * FROM {self._table_name} WHERE publication_date like :publication_date"
                self._cursor.execute(query, {'publication_date': pub_date})
                logger.debug('Query performed to fetch rows according to publishing date.')
        elif source != '':
            query = f"SELECT * FROM {self._table_name} WHERE feed_url=:source"
            self._cursor.execute(query, {'source': source})
            logger.debug('Query performed to fetch rows according to source.')
        else:
            sys.exit("Neither source nor date provided to perform query. Program terminated. Try again.")

    def retrieve_from_db(self, date: str, source: str, limit: int) -> List[tuple]:
        """Retrieves records from database according to arguments specified

        Args:
            date: News publishing date
            source: Feed source
            limit: Limit of the to be fetched records

        Returns:
            Fetched records
        """
        self._query_db(date, source)

        if limit is not None:
            return self._cursor.fetchmany(limit)
        else:
            return self._cursor.fetchall()
