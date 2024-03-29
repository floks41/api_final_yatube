# Проект API для социальной платформы блогеров.

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)

- Python 3.9
- Django 2.2.16
- Django REST framework 3.12.4
- Django REST framework simple JWT 4.7.2
### Разработчик:

👨🏼‍💻Олег Чужмаров: https://github.com/floks41

## Описание

Назначение проекта: предоставление программного интерфейса (api) к социальной платформе блогеров. Создание и развитие api позволит подключить к бекенду платформы иные приложения, в том числе, веб-фронтенд для пользователей интернет-браузеров, десктопные и мобильные приложения.


## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:floks41/api_final_yatube.git
```

Перейти в каталог проекта

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt, для перед этим обновить менеджер пакетов:

```
python3 -m pip install --upgrade pip
```

pip install -r requirements.txt
Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Перейти в каталог основного приложения

```
cd yatube_api
```

## Как пользоваться

Api имеет несколько эндпоинтов.

Полная документация доступна после запуска приложения по эндпоинту `/redoc/`.

### Доступ к api

Аутентифицированным пользователям разрешено изменение и удаление своего контента; в остальных случаях доступ предоставляется только для чтения, эндпоинт `/follow/` доступен только аутентифицированным пользователям.

Для аутентификации используются JWT-токены.

**Получить JWT-токен: POST** `/api/v1/jwt/create/`

Пример запроса. Все поля обязательны.

```json
{
    "username": "string",
    "password": "string"
}
```

Пример ответа:

```json
{
    "refresh": "здесь токен обновления",
    "access": "здесь токен доступа"
}
```

**Обновить JWT-токен: POST** `/api/v1/jwt/refresh/`

Пример запроса. Все поля обязательны.

```json
{
    "refresh": "здесь токен"
}
```

**Проверить JWT-токен: POST** `/api/v1/jwt/verify/`

Пример запроса. Все поля обязательны.

```json
{
    "token": "здесь токен"
}
```

### Посты

**GET** `/api/v1/posts/` c параметрами limit и offset возвращает список постов с элементами пагинации

Пример ответа:

```json
{
    "count": 123,
    "next": "http://api.example.org/accounts/?offset=400&limit=100",
    "previous": "http://api.example.org/accounts/?offset=200&limit=100",
    "results": [{
        "id": 0,
        "author": "string",
        "text": "string",
        "pub_date": "2021-10-14T20:41:29.648Z",
        "image": "string",
        "group": 0
    }]
}
```

**POST** `/api/v1/posts/` создание поста

Пример запроса. Поле `text` обязательное.

```json
{
    "text": "string",
    "image": "string",
    "group": 0
}
```

Пример ответа:

```json
{
    "id": 0,
    "author": "string",
    "text": "string",
    "pub_date": "2019-08-24T14:15:22Z",
    "image": "string",
    "group": 0
}
```

Получить отдельный пост **GET** `/api/v1/posts/{id}/`. Также доступно обновление **PUT**, **PATCH**, поля аналогичны запросу на создание поста. Запрос **DELETE** без параметров.

### Комментарии

**GET** `/api/v1/posts/{post_id}/comments/` запрос комментариев к посту.

Пример ответа:

```json
[
    {
        "id": 0,
        "author": "string",
        "text": "string",
        "created": "2019-08-24T14:15:22Z",
        "post": 0
    }
]
```

**POST** `/api/v1/posts/{post_id}/comments/` создание комментария к посту. Пример запроса. Поле `text` обязательное.

```json
{
    "text": "Текст комментария"
}
```

Пример ответа:

```json
{
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2019-08-24T14:15:22Z",
    "post": 0
}
```

**GET** `/api/v1/posts/{post_id}/comments/{id}/` запрос комментария.

Пример ответа:

```json
{
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2019-08-24T14:15:22Z",
    "post": 0
}
```

Также доступно обновление **PUT**, **PATCH**, поля аналогичны запросу на создание комментария. Запрос **DELETE** без параметров.

### Сообщества

**GET** `/api/v1/groups/` запрос перечня сообществ.

Пример ответа:

```json
[
    {
        "id": 0,
        "title": "string",
        "slug": "string",
        "description": "string"
    }
]
```

**GET** `/api/v1/groups/{id}/` запрос информации о сообществе.

Пример ответа:

```json
{
    "id": 0,
    "title": "string",
    "slug": "string",
    "description": "string"
}
```

### Подписки

Доступны только аутентифицированным пользователям.

**GET** `/api/v1/follow/` Возвращает все подписки пользователя, сделавшего запрос. Анонимные запросы запрещены.

Пример ответа:

```json
[
   {
       "user": "string",
       "following": "string"
   }
]
```

**POST** `/api/v1/follow/` Создание подписки пользователя от имени которого сделан запрос на пользователя переданного в теле запроса. Анонимные запросы запрещены. Пример запроса, поле `following` обязательно.

```json
{
    "following": "username"
}
```

Пример ответа:

```json
{
    "user": "string",
    "following": "string"
}
```
