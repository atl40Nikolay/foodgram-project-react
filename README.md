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
### Примеры запросов и ответов:
- Список пользователей
GET запрос
```
http://localhost/api/users/
```
код ответа 200
```
{
  "count": 123,
  "next": "http://localhost/api/users/?page=4",
  "previous": "http://localhost/api/users/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": false
    }
  ]
}
```

- Регистрация пользователя
POST запрос
```
http://localhost/api/users/
```
```
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
```
код ответа 201
```
{
  "email": "vpupkin@yandex.ru",
  "id": 0,
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин"
}
```
код ответа 400
```
{
  "field_name": [
    "Обязательное поле."
  ]
}
```

- Профиль пользователя
GET запрос
```
http://localhost/api/users/{id}/
```
код ответа 200
```
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": false
}
```
код ответа 404
```
{
  "detail": "Страница не найдена."
}
```

- Текущий пользователь
GET запрос
```
http://localhost/api/users/me/
```
код ответа 200
```
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": false
}
```
код ответа 401
```
{
  "detail": "Учетные данные не были предоставлены."
}
```

- Получить токен авторизации
POST запрос
```
http://localhost/api/auth/token/login/
```
```
{
  "password": "string",
  "email": "string"
}
```
код ответа 201
```
{
  "auth_token": "string"
}
```

- Удаление токена
POST запрос
```
http://localhost/api/auth/token/logout/
```
код ответа 204
```
null
```
код ответа 401
```
{
  "detail": "Учетные данные не были предоставлены."
}
```

- Cписок тегов
GET запрос
```
http://localhost/api/tags/
```
код ответа 200
```
[
  {
    "id": 0,
    "name": "Завтрак",
    "color": "#E26C2D",
    "slug": "breakfast"
  }
]
```

- Получение тега
GET запрос
```
http://localhost/api/tags/{id}/
```
код ответа 200
```
{
  "id": 0,
  "name": "Завтрак",
  "color": "#E26C2D",
  "slug": "breakfast"
}
```
код ответа 404
```
{
  "detail": "Страница не найдена."
}
```

- Список рецептов
GET запрос
```
http://localhost/api/recipes/
```
код ответа 200
```
{
  "count": 123,
  "next": "http://localhost/api/recipes/?page=4",
  "previous": "http://localhost/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://localhost/media/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

### Документация:

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