from sqlite_to_postgres.model_dataclasses import Genre, Genre_Film_work, \
    Person, Person_Film_work, Film_work


class SQLiteExtractor:
    def __init__(self, connection):
        self.connection = connection
        self.dclasses = [Genre, Person, Film_work, Genre_Film_work, Person_Film_work]
        self.dnames = [str(dclass.__name__).lower() for dclass in self.dclasses]

    def extract_movies(self, batch_size):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        table_names = [name[0].lower() for name in tables]
        tables_ordered = []  # This is needed, cause some tables has rows with FK
        for dname in self.dnames:
            tables_ordered.append(tables[table_names.index(dname)])
        for table in tables_ordered:
            table_name = table[0]
            cursor.execute(f"SELECT * FROM {table_name};")
            columns = [description[0] for description in cursor.description]
            while True:  # while rows := cursor.fetchmany(batch_size)
                rows = cursor.fetchmany(batch_size)
                if not rows:
                    break
                yield {table_name: [dict(zip(columns, row)) for row in rows]}

    def get_sqlite_indexes(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(f"PRAGMA index_list({table_name})")
        indexes = cursor.fetchall()
        index_data = []
        for index in indexes:
            if not index[1].startswith("sqlite_autoindex"):
                index_name = index[1]
                cursor.execute(f"PRAGMA index_info({index_name})")
                columns = cursor.fetchall()
                column_names = [column[2] for column in columns]
                index_data.append((index_name, column_names))
        return index_data

    def get_sqlite_foreign_keys(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        foreign_keys = cursor.fetchall()
        return foreign_keys
