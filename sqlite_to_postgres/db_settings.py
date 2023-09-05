import logging
import os

from dotenv import load_dotenv

log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs/load_data.log")
if not os.path.exists(log_path):  # Если файл не существует, создаем его и устанавливаем настройки логирования
    with open(log_path, 'w'):
        pass
logging.basicConfig(filename=log_path, level=logging.ERROR)
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
load_dotenv(dotenv_path)

dsl = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT'),
}
sqlite_db_name = os.environ.get('SQLITE_DB_NAME')
