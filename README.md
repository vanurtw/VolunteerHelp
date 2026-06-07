
### Компоненты системы:

- **Django** - основной бэкенд фреймворк
- **PostgreSQL** - база данных
- **Nginx** - обратный прокси и статика
- **Adminer** - веб-интерфейс управления БД
- **Docker** - контейнеризация всех сервисов
- **JWT** -  реализация токенов
  
## 🚀 Запуск проекта

### 1. Клонируйте репозиторий
```https://github.com/vanurtw/VolunteerHelp.git```


### 2. Настройте переменные окружения 
Создайте файл ***.env*** на одном уровне с фаулом **compose.yml** 

Добавте в него переменные среды:

- *DB_NAME=DB_NAME*
- *DB_USER=DB_USER*
- *DB_PASSWORD=DB_PASSWROD*
- *DB_HOST=dbps*
- *DB_PORT=5432*
- *SECRET_KEY=SEKRET_KEY*

### 3. Запустите проект через Dcoker

Запуск всех контейнеров: ```docker compose up --build```

Примените миграции: ```docker-compose exec volunteer_help python manage.py migrate```

Создайте суперпользователя: ```docker-compose exec volunteer_help python manage.py createsuperuser``` - опционально
если загружать фикстуры то он там уже будет

Можно загрузить начальные данные для БД (опционально): ```docker-compose exec volunteer_help python manage.py loaddata db.json```


### Доступ к сервисам

|Сервис|URL|Описание|
|------|---|--------|
|🚀 API	|http://127.0.0.1:80|REST API
👨‍💼 Adminer|http://127.0.0.1:8080/|Управление БД
👑 Админка Django|http://127.0.0.1:80/admin/|Администрирование
📚 API Документация|http://127.0.0.1:80/swagger/|Swagger/Redoc
