# Используем официальный образ Python 3.13.9 на базе Debian Bookworm
FROM python:3.13.9-bookworm

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем системные зависимости
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gettext \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем непривилегированного пользователя с UID 1000
RUN groupadd -r django && useradd -r -g django -u 1000 django

# Создаем необходимые директории и предоставляем права
RUN mkdir -p db media staticfiles \
    && chown -R django:django /app \
    && chmod -R 755 /app/db /app/media

# Переключаемся на непривилегированного пользователя
USER django

# Сollectstatic файлы (выполняется от имени пользователя django)
RUN python manage.py collectstatic --noinput

# Устанавливаем точку входа
ENTRYPOINT ["./entrypoint.sh"]

# Команда по умолчанию для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]