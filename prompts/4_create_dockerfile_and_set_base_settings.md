### Создай Docker-образ 
на основе официального образа python:3.13.9-bookworm (Debian Bookworm) со следующими требованиями:

1. Зависимости и игнорирование файлов
Добавь файл requirements.txt с необходимыми Python-зависимостями (включая Django 5.2.7).
Создай файл .dockerignore и исключи из сборки:
```
db/
media/
staticfiles/
.venv/
```

2. Расположение базы данных
Настрой проект так, чтобы файл SQLite (db.sqlite3) сохранялся в папке ./db (в корне проекта).
Обнови settings.py, указав путь к базе данных:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db' / 'db.sqlite3',
    }
}

3. Настройки для запуска в Cloud.ru Container Apps
Добавь в settings.py следующие параметры:

```python
import os

CONTAINER_APP_NAME = os.environ.get("CONTAINER_NAME", "-")  # будет установлен средой Cloud.ru Container Apps

ALLOWED_HOSTS = [
    f'{CONTAINER_APP_NAME}.containerapps.ru',
    f'{CONTAINER_APP_NAME}.internal.containers.cloud.ru',
    'localhost',
    '127.0.0.1',
]

CSRF_TRUSTED_ORIGINS = [
    f'https://{CONTAINER_APP_NAME}.containerapps.ru',
    f'https://{CONTAINER_APP_NAME}.internal.containers.cloud.ru',
]

# Django пытается изменить права доступа к загруженным файлам — отключаем это поведение
FILE_UPLOAD_PERMISSIONS = None
```

4. Пользователь и права доступа
В Dockerfile создай непривилегированного пользователя с UID 1000.
Предоставь этому пользователю права на запись в папки:
./db (для базы данных)
./media (для загружаемых изображений)

5. В Dockerfile добавь 
RUN python manage.py collectstatic --noinput
ENTRYPOINT entrypoint.sh 
в котором: 
- запусти миграции
- запусти django команду для создания admin пользователя create-admin-user
- запусти django команду fill_records
CMD добавь запуск runserver

6. Добавь в Readme.md способ запуска приложения через Docker
