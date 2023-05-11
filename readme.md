# Сервис REST VK Friends

#### Данный сервис дает пользователю следующие возможности:
- зарегистрировать нового пользователя
- отправить одному пользователю заявку в друзья другому
- принять/отклонить пользователю заявку в друзья от другого пользователя
- посмотреть пользователю список своих исходящих и входящих заявок в друзья
- посмотреть пользователю список своих друзей
- получить пользователю статус дружбы с каким-то другим пользователем 
    (нет ничего / есть исходящая заявка / есть входящая заявка / уже друзья)
- удалить пользователю другого пользователя из своих друзей
- если пользователь1 отправляет заявку в друзья пользователю2, а пользователь2 отправляет заявку пользователю1, 
    то они автоматом становятся друзьями, их заявки автоматом принимаются

#### Запуск проекта:
- Устоновить Python 3.9 и активировать виртуальное окружение
- Установить все зависимости из файла reqirements.txt командой 
    `pip install -r requirements.txt`
- В режиме виртуально окружения (venv) из корневой папки проекта выполнить следующие команды
- создать базу данных и выполнить миграции для базы данных
    `python manage.py makemigrations`
    `python manage.py migrate`
- Создать администратора проекта
    `python manage.py createsuperuser`
- Запустить сервер проекта
    `python manage.py runserver` 
    
#### Запуск проекта в контейнере Docker с использование Docker Compose:
- Установить Docker и Docker Compose:
    Выполнить в терминале следующие команды в тернинале (Ubuntu Server): 

- Установка Docker:

``` 
    sudo apt install apt-transport-https ca-certificates curl software-properties-common 
    && 
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - 
    && 
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable" 
    && 
    sudo apt update && apt-cache policy docker-ce && sudo apt install docker-ce 
    && 
    sudo apt install docker-ce && sudo systemctl status docker
    &&
    sudo systemctl start docker && sudo systemctl enable docker
```

- Установка Docker Compose версии 2.17.3:
    (проверить последнюю версию на сайте docker compose и изменить команду)

```
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.17.3/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
    &&
    sudo chmod +x /usr/local/bin/docker-compose
    &&
    docker-compose --version
```

Если вывод в терминале: 
Docker Compose version v2.17.3 
значит все уствновлено правильно

- При необходимости подключить Nginx и PostgreSQL (убрать комментарий в файле docker-compose.yaml) и 
    изменить настройки в файле settings.py в разделе DATABASES (выбрать другое подключение)
- Для запуска всех небходимых контейнеров из корневой папки проекта выполнить команду:     

```
docker-compose -f docker-compose.yml up -d --build
```
после запуска всех контейнеров проект будет доступел по адресу:
http://<host name>:8080/ или http://0.0.0.0:8080/

#### Основные возможности сервиса и примеры выполнения запросов:

- Регистрация нового пользователя:
Отправить POST запрос на адрес: `http://<host_name>:8000/auth/users/` 
в теле запроса указать:
    
```
{
    "username": "test5",
    "email": "test5@mail.ru",
    "password": "1234qwer5"
}
```
ответ от сервера:

```
{
    "email": "test5@mail.ru",
    "username": "test5",
    "id": 6
}
```
- Получить JWT Token для зарегистрированного пользавателя и 
для доступа к информации только для зарегистрированных пользователей.
Отправить `POST` запрос на адрес `http://<host_name>:8000/auth/jwt/create/`  
В теле запроса указать:
```
{
    "username": "test7",
    "password": "1234qwer7"
}
```
Ответ от сервера:
```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4Mzg0NjAwMSwiaWF0IjoxNjgzNzU5NjAxLCJqdGkiOiJjNDIzOTM1MzAwNzM0MWYwYjIyMzZkN2M2MTcyODZmMyIsInVzZXJfaWQiOjh9.upECEObLLb7hn_v2BNXlz_U_wEE7RiY0u-Ey_pjFLoY",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzNzU5OTAxLCJpYXQiOjE2ODM3NTk2MDEsImp0aSI6IjNmMGNjNmJhYmVmZDQ5ZGFiOTQzZGZkZTg4MDc5YTI1IiwidXNlcl9pZCI6OH0.BCc3GRxFt8MFoZT8D32xFIDhhExTOiytUXo9cK6ZwH8"
}
```
-Для получения информации только для зарегестррированныз пользователей 
небходимо при каждом запросе в заголовке Authorization указать через пробел 
ключевое слово JWT и access token, например:
```
JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzNzU5OTAxLCJpYXQiOjE2ODM3NTk2MDEsImp0aSI6IjNmMGNjNmJhYmVmZDQ5ZGFiOTQzZGZkZTg4MDc5YTI1IiwidXNlcl9pZCI6OH0.BCc3GRxFt8MFoZT8D32xFIDhhExTOiytUXo9cK6ZwH8
```

- Посмотреть всех пользователей:
Отправить GET запрос на адрес: `http://<host_name>:8000/api/` 

ответ сервера:
```
{
    "id": 3,
    "username": "test222",
    "first_name": "test22",
    "last_name": "test22",
    "email": "test222@mail.ru"
},
{
    "id": 4,
    "username": "test3",
    "first_name": "test3",
    "last_name": "test3",
    "email": "test3@mail.ru"
},
```
- Отправить одному пользователю заявку в друзья другому:
Отправить `POST` запрос на адрес вида: `http://<host_name>:8000/api/friends/friendship_requests/?user=6&friend=7`
где в параметрах запроса указать `user=user_id` и `friend=friend_id`(user_id получателя).
При коррктном запросе ответ от сервера должен быть:
```
{
    "Request SENT": {
        "id": 13,
        "sender": 6,
        "receiver": 7,
        "friendship_status": "SENT",
        "is_active": true
    }
}
```
При ошибочно отправленной повторной заявке в друзья от одного и пользователя, 
ответ от сервера должен быть:
```
{
    "Request SENT": "request is already exist"
}
```  
Если при оправке заявки в друзья другому пользователю на сервисе есть от него входящая заявка, 
то заявка автоматически подтверждается и ответ от сервера должен быть:
```
{
    "Request SENT": {
        "Friendship Status": "is friended"
        }
}
```  

- Чтобы принять/отклонить пользователю заявку в друзья от другого пользователя
необходимо отправить PUT запрос на адрес вида:
`http://<host_name>:8000/api/friends/friendship_requests/13/?user=7&friend=6&action=confirmed`
где `13` соответствует `id` запроса в друзья, также в параметрах запроса нужно указать 
`user=user_id` , `friend=friend_id`(user_id получателя) и `action=confirmed`(declined) 
чтобы принять(отклонить) заявку. 
При корректном запросе ответ от сервера должен быть:
```
{
    "Request CONFIRMED": {
        "Friendship Status": "is friended"
       }
}
```
или при отклонении запроса(declined) в друзья ответ должен быть:
```
{
    "Request SENT": {
        "id": 13,
        "sender": 6,
        "receiver": 7,
        "friendship_status": "DECLINED",
        "is_active": true
    }
}
```

- Чтобы посмотреть пользователю список своих исходящих и входящих заявок в друзья нужно 
отправить `GET` запрос на адрес вида: `http://<host_name>:8000/api/friends/friendship_requests/?user=3&action=s`
где в параметрах запроса указать `user=user_id` и `action=s` (для исходящих запросов) или `action=r` 
(для входящих запросов). Если такие заявки присетствуют, то ответ от сервера будет:
```
[
    {
        "id": 5,
        "friendship_status": "SENT",
        "is_active": true,
        "create_date": null,
        "update_date": "2023-05-09T01:42:15.164802+03:00",
        "sender": 3,
        "receiver": 2
    },
    {
        "id": 15,
        "friendship_status": "SENT",
        "is_active": true,
        "create_date": "2023-05-09T03:05:22.292319+03:00",
        "update_date": "2023-05-09T03:05:22.304096+03:00",
        "sender": 3,
        "receiver": 6
    }
]
```
если записей нет, то ответ будет:
```
[]
```
- Чтобы посмотреть пользователю список своих друзей необходимо отправить `GET` запрос с 
параметрами на адрес вида: `http://127.0.0.1:8000/api/friends/user_friends/?user=5 ` , 
где  указать `user=user_id`. 
Если у пользователя есть друзья то ответ от сервера будет:
```
[
    {
        "id": 8,
        "is_active": true,
        "create_date": "2023-05-08T01:15:37.784518+03:00",
        "update_date": "2023-05-08T01:15:37.784555+03:00",
        "user1": 3,
        "user2": 5
    },
    {
        "id": 9,
        "is_active": true,
        "create_date": "2023-05-08T01:15:45.673094+03:00",
        "update_date": "2023-05-08T01:15:45.673131+03:00",
        "user1": 2,
        "user2": 5
    }
]
```
А если друзей нет, то ответ будет:
```
[]
```
- Чтобы получить пользователю статус дружбы с каким-то другим пользователем необходимо 
отправить `GET` запрос с параметрами на адрес вида: `http://<host_name>:8000/api/friends/get_friends_status/?user=4&friend=2` ,
в парамерах запроса указать `user=user_id` , `friend=friend_id`(user_id друга).
При корректном запросе ответы сервера могут быть:
Если уже друзья:
```
{
    "Friendship Status": [
        "is friended"
    ]
}
```

Если есть исходящие заявки:
```
{
    "Friendship Status": [
        "sent request"
    ]
}
```
Если есть входящие заявки:
```
{
    "Friendship Status": [
        "received request"
    ]
}
```
Если не друзья и нет входящей или исходящей заявоки:
```
{
    "Friendship Status": [
        "no data"
    ]
}
```
- Чтобы пользователю удалить другого пользователя из своих друзей необходимо 
отправить `DELETE` запрос с параметрами на адрес вида: `http://<host_name>:8000/api/friends/user_delete_friend/?user=5&friend=3` , 
где парамерах запроса указать `user=user_id` , `friend=friend_id`(user_id друга). 
При корректном запросе ответ сервера должен быть:
```
{
    "id": 10,
    "is_active": false,
    "create_date": "2023-05-09T01:16:08.568454+03:00",
    "update_date": "2023-05-09T02:55:13.397219+03:00",
    "user1": 2,
    "user2": 4
}
```
Если данные введены некорректно, то ответ будет:
```
{
    "error": "no valid data"
}
```
-Для просмотра OPEN API спецификации необходимо перейти по одному изадресов:
    - Спецификация в формате API или JSON - `http://<host_name>:8000/openapi/`
    - Спецификация c Swagger Ui - `http://<host_name>:8000/swagger-ui/`
    - Спецификация c Redoc Ui - `http://<host_name>:8000/redoc/`
