# Пока что реализовал без multistage сборки
FROM python:3.9
LABEL authors="mruax"


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

# Устанавливаем зависимости для разработки
RUN pip install --no-cache-dir -r dev-requirements.txt

# Добавляем PYTHONPATH для отдельных модулей (необязательно для production)
# ENV PYTHONPATH="/sqlite_to_postgres:${PYTHONPATH}"

# Запускаем команду для выполнения миграций и запуска веб-сервера Django локально
# CMD python /app/manage.py migrate && python /app/manage.py runserver 0.0.0.0:8000

# Миграции и запуск uWSGI веб-сервера
CMD python /app/manage.py migrate && uwsgi --ini /app/uwsgi.ini