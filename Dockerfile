# STAGE 1: production
# Используем образ Python как базовый
# FROM python:3.9 as production
FROM python:3.9
LABEL authors="mruax"

# TODO: Разобраться с пользователями и multistage сборкой
# Создаем непривилегированного пользователя "myuser" с UID и GID равными 1000
# RUN useradd -m myuser -u 1000
# Задаем пользовательский контекст для последующих команд внутри контейнера
# USER myuser

# Устанавливаем переменные среды
ENV PYTHONUNBUFFERED 1

# Установка системных зависимостей (ping для тестирования && apt-get install -y iputils-ping)
RUN apt-get update && apt-get install -y build-essential  # && mkdir /logs

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем основные зависимости проекта
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код проекта внутрь контейнера
COPY . /app/

# Указываем файл .env в директории config/ в качестве источника переменных среды
ENV ENV_FILE_PATH=/app/config/.env

# STAGE 2: development
# FROM production as development

# Устанавливаем зависимости для разработки
RUN pip install --no-cache-dir -r dev-requirements.txt

# Добавляем PYTHONPATH для отдельных модулей (необязательно для production)
# ENV PYTHONPATH="/sqlite_to_postgres:${PYTHONPATH}"

# Запускаем команду для выполнения миграций и запуска веб-сервера Django локально
# CMD python /app/manage.py migrate && python /app/manage.py runserver 0.0.0.0:8000

# Миграции и запуск uWSGI веб-сервера
CMD python /app/manage.py migrate && uwsgi --ini /app/uwsgi.ini