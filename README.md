# OPENAPI
Сервис уведомлений
### Installation:

Чтобы скачать репозиторий наберите в командной строке:
```sh
git clone -b openapi_v1 https://gitlab.com/SergeyKondratyevVl/my_test_task.git
```

### Recommended requirements installation via requirements.txt file
```sh
pip install -r requirements.txt
```

Также вам необходимо будет настроить файл .env.
- POSTGRES_ENGINE
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_HOST
- POSTGRES_PORT
- REDIS_HOST
- REDIS_PORT


### Usage instruction:
Вы можете просмотреть возможности сервиса в Swagger UI. В сервисе реализована возможность CRUD для клиентов и рассылок. Также реализовано тестирование сервиса. Имеется возможность запуска сервиса с помощью docker-compose. tag для пользователя указывается единственным словом, например, python. Код мобильного оператора определяется как 3 цифры после первой семёрки; после создания вы можете вручную изменить его. Поле filtering указывается либо как tag:, либо как phone_index:<phone_index>.

### Start project:
После этого вернуться в папку сервиса и проделать следующие команды.
```sh
python manage.py makemigrations mailing
python manage.py migrate
python manage.py runserver
```

Чтобы запустить проект с помощью docker, то:
```sh
docker-compose up --build
```

Файл .env
- POSTGRES_ENGINE=django.db.backends.postgresql_psycopg2
- POSTGRES_DB=db
- POSTGRES_USER=user
- POSTGRES_PASSWORD=password
- POSTGRES_HOST=postgres
- POSTGRES_PORT=5432
- REDIS_HOST=redis
- REDIS_PORT=6379
