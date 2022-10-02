##  Проект "Foodgram"

![Actions Status](https://github.com/atl40Nikolay/foodgram-project-react/actions/workflows/myworkflow.yml/badge.svg)

### Описание проекта:

Ваш дипломный проект — сайт Foodgram, «Продуктовый помощник». Написан онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
```
http://51.250.23.101
```

### Технологии:

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat-square&logo=Docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)


### Как запустить проект локально:

* Установите Docker.

Параметры запуска описаны в файлах `docker-compose.yml` и `nginx.conf` которые находятся в директории `infra/`.

* Cоздайте файл `.env` в директории `/infra/` с содержанием:
```
SECRET_KEY=секретный ключ django
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

* Запустите docker compose:
```
docker-compose up -d
```
> После сборки запускаются 3 контейнера:
> 1. контейнер базы данных **infra_db_1**
> 2. контейнер приложения **infra_backend_1**
> 3. контейнер http-сервера **infra_nginx_1**
* Примените миграции:
```
docker-compose exec backend python manage.py migrate
```
* Загрузите ингредиенты:
```
docker-compose exec backend python manage.py loaddata data/data.json
```
* Создайте администратора:
```
docker-compose exec backend python manage.py createsuperuser
```
* Соберите статику:
```
docker-compose exec backend python manage.py collectstatic --noinput
```

### Документация, примеры запросов и ответов:

Обратившись к эндпоинту api/docs/, вы можете ознакомиться с документацией сервиса, посмотреть доступные варианты api-запросов к серверу и его ответов.

### Автор проекта:

для теста админки
```
admin@cyber.org
Password13@
```

Николай Журавлёв
[![Me](https://img.shields.io/badge/https%3A%2F%2Fgithub.com%2Fatl40Nikolay-Николай%20Журавлёв-green)](https://github.com/atl40Nikolay)

atl40@yandex.ru