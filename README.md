# movie cinema webserver


## Run with Docker Compose
1. Create .env with all settings (see .env.example)
2. Collect static with `python manage.py collectstatic`
3. Run `docker-compose up --build`

## Run locally (experimental)
This method may need changes in some files/dirs paths and dns names to local ips.
1. Install requirements and dev-requirements
2. Create .env with all settings (see .env.example)
3. Migrate db data with `python /app/manage.py migrate`
4. Collect static with `python manage.py collectstatic`
5. Choose server to run (uwsgi with `uwsgi --ini /app/uwsgi.ini` or django with `python /app/manage.py runserver 0.0.0.0:8000`)

## Data migration (sql -> postgres)
Follow these steps to migrate data from db.sqlite to postgres (using Docker Compose method):
1. Create /logs/load_data.log locally
2. Build and up Docker Compose and enter django_webserver container terminal
3. Run `export PYTHONPATH="/sqlite_to_postgres:${PYTHONPATH}"`
4. Run `python sqlite_to_postgres/load_data.py`

You need to change DNS container names to local IPs for migrating data locally (and maybe some other settings).

## Troubleshooting
There are possible errors that may occur if something went wrong. Here are some examples how to try fix them.

### logs
Sometimes you need to manually create /logs directory and needed .log files.

### sql -> postgres
Sometimes may cause errors in postgres_model.py. Use scheme name on INSERT operations.

### Docker Compose
If Docker outputs errors about permissions then it may be caused by following things (most of):
* Unnamed volumes in docker-compose.yml
* Incorrect chown/chmod on some directories (ex. pgdata). Use your user + docker/postgres (or other group) and 700 rights (or even more protected) because some directories need to be chown by user who started server.

Возможные записи в сервисе db:
- "pgdata:/var/lib/postgresql/data"
- ./pgdata:/var/lib/postgresql/data  # (instead use unnamed volume when troubles with permissions)

Также тк compose ищет переменные, указанные через $ в .env-файле по умолчанию рядом с .yml, необходимо указать его в корневой папке.

### Paths
There are plenty of errors caused by incorrect paths (locally or in Docker). Be careful with Docker Compose volumes and .env file.