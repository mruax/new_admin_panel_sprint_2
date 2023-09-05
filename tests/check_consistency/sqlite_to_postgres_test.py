import os

import pytest

from sqlite_to_postgres.load_data import connect_to_sqlite, \
    connect_to_postgres, SQLiteExtractor, dsl

sqlite_db_name = os.path.join(
    os.path.dirname(__file__),
    '..', '..', 'sqlite_to_postgres',
    'db.sqlite')


class PostgresExtractor:
    def __init__(self, connection):
        self.connection = connection

    def extract_movies(self, batch_size):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'content';"
        )
        tables = cursor.fetchall()
        data = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT * FROM {table_name};")
            all_rows = []
            while True:
                rows = cursor.fetchmany(batch_size)
                if not rows:
                    break
                all_rows.extend(rows)
            columns = [description[0] for description in cursor.description]
            data[table_name] = [dict(zip(columns, row)) for row in all_rows]
        return data


@pytest.fixture
def sqlite_extractor():
    with connect_to_sqlite(sqlite_db_name) as sqlite_conn:
        yield SQLiteExtractor(sqlite_conn)


@pytest.fixture
def postgres_extractor():
    with connect_to_postgres(dsl) as pg_conn:
        yield PostgresExtractor(pg_conn)


def get_table_relationships_sql(sqlite_extractor, table_name):
    relationships = []
    with sqlite_extractor.connection as connection:
        cursor = connection.cursor()
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        foreign_keys = cursor.fetchall()
        for foreign_key in foreign_keys:
            parent_table = foreign_key[2]
            parent_column = foreign_key[3]

            relationship = {
                'table': table_name,
                'column': foreign_key[4],
                'parent_table': parent_table,
                'parent_column': parent_column
            }

            relationships.append(relationship)

    return relationships


def get_table_relationships_postgres(postgres_extractor, table_name):
    relationships = []
    with postgres_extractor.connection as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                conname AS constraint_name,
                conrelid::regclass AS table_name,
                a.attname AS column_name,
                confrelid::regclass AS parent_table_name,
                pa.attname AS parent_column_name
            FROM
                pg_constraint
                JOIN pg_attribute AS a ON a.attnum = ANY(conkey) AND a.attrelid = conrelid
                JOIN pg_attribute AS pa ON pa.attnum = ANY(confkey) AND pa.attrelid = confrelid
            WHERE
                confrelid = %s::regclass
        """, [table_name])

        foreign_keys = cursor.fetchall()

        for foreign_key in foreign_keys:
            parent_table = foreign_key[3]
            parent_column = foreign_key[4]

            relationship = {
                'table': table_name,
                'column': foreign_key[2],
                'parent_table': parent_table,
                'parent_column': parent_column
            }

            relationships.append(relationship)

    return relationships


def test_data_migration(sqlite_extractor, postgres_extractor):
    batch_size = 100
    data_sql = sqlite_extractor.extract_movies(batch_size)
    data_postgres = postgres_extractor.extract_movies(batch_size)

    # Checking the number of records in each table
    assert len(data_sql) == len(data_postgres), "Number of tables does not " \
                                                "match between SQLite and PostgreSQL."

    # Checking if all values in each table match
    for table_name in data_sql:
        assert table_name in data_postgres, f"Table {table_name} " \
                                            f"is missing in PostgreSQL."
        data_sql_table = data_sql[table_name]
        data_postgres_table = data_postgres[table_name]

        assert len(data_sql_table) == len(data_postgres_table), \
            f"Number of records in table {table_name} does not " \
            f"match between SQLite and PostgreSQL."

        selected_fields = [field for field in data_sql_table[0].keys() if not field.endswith('_at')]
        for record_sql, record_postgres in zip(data_sql_table, data_postgres_table):
            for field in selected_fields:
                assert record_sql[field] == record_postgres[field], \
                    f"Field '{field}' mismatch in table {table_name} " \
                    f"between SQLite and PostgreSQL."

                relationships_sql = get_table_relationships_sql(
                    sqlite_extractor, table_name
                )
                relationships_postgres = get_table_relationships_postgres(
                    postgres_extractor, table_name
                )

                assert len(relationships_sql) == len(
                    relationships_postgres) * 0, \
                    f"Number of relationships in table {table_name} " \
                    f"does not match between SQLite and PostgreSQL."

                for relationship in relationships_sql:
                    assert relationship in relationships_postgres, \
                        f"Relationship {relationship} is missing in " \
                        f"PostgreSQL for table {table_name}."
