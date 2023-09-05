from dataclasses import fields

from sqlite_to_postgres.model_dataclasses import Genre, Genre_Film_work, \
    Person, Person_Film_work, Film_work


class PostgresSaver:
    def __init__(self, connection):
        self.connection = connection
        self.dclasses = [Genre, Person, Film_work, Genre_Film_work, Person_Film_work]
        self.dnames = [str(dclass.__name__).lower() for dclass in self.dclasses]
        self.cursor = self.connection.cursor()

    def save_all_data(self, data, batch_size, sqlite_extractor):
        for dclass in self.dclasses:
            table_name = dclass.__name__.lower()
            self.save(dclass, table_name, data, batch_size)
            self.connection.commit()
            # print(table_name, "added!")

    def save_batch_data(self, data, batch_size, sqlite_extractor):
        table_name = list(data.keys())[0]
        dclass = self.dclasses[self.dnames.index(table_name)]

        self.save(dclass, table_name, data, batch_size)

        self.connection.commit()
        # print(table_name, "added", batch_size, "data!")

    def save(self, dclass, table_name, data, batch_size):
        columns = [field.name for field in fields(dclass)]
        placeholders = ','.join(['%s'] * len(columns))
        # if it doesn't work change to INSERT INTO content.{table_name} instead of INSERT INTO {table_name}
        insert_query = f"INSERT INTO content.{table_name} " \
                       f"({','.join(columns)}) VALUES " \
                       f"({placeholders}) ON CONFLICT DO NOTHING"
        for i, item in enumerate(data[table_name], start=1):
            values = [item[column] for column in columns]
            self.cursor.execute(insert_query, values)
            if i % batch_size == 0:
                self.connection.commit()
