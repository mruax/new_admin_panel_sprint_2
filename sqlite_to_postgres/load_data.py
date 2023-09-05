import sqlite3
from contextlib import contextmanager

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from db_settings import logging, dsl, sqlite_db_name
from sqlite_to_postgres.postgres_model import PostgresSaver
from sqlite_to_postgres.sqlite_model import SQLiteExtractor


@contextmanager
def connect_to_sqlite(sqlite_db_name):
    conn = sqlite3.connect(sqlite_db_name)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@contextmanager
def connect_to_postgres(dsl):
    conn_ps = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    try:
        yield conn_ps
        conn_ps.commit()
    except Exception as error:
        logging.error(str(error))
        conn_ps.rollback()
    finally:
        conn_ps.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Main method to load data from SQLite to Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    batch_size = 100  # used for fetchmany/commit functions
    data = sqlite_extractor.extract_movies(batch_size)
    for batch_data in data:
        postgres_saver.save_batch_data(batch_data, batch_size, sqlite_extractor)


if __name__ == '__main__':
    with connect_to_sqlite(sqlite_db_name) as sqlite_conn, connect_to_postgres(dsl) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
