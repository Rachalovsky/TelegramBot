# Telegram Bot

Этот проект представляет собой телеграм-бота, написанного на Pyrogram, который использует конечный автомат состояний (FSM) для управления состояниями пользователей. Бот взаимодействует с базой данных PostgreSQL через асинхронные запросы, используя SQLAlchemy.

---
## Описание

Телеграм-бот позволяет пользователям регистрироваться, управлять задачами и взаимодействовать с базой данных через асинхронные запросы. Проект структурирован таким образом, чтобы быть легко расширяемым и поддерживаемым.

---
## Установка

Для установки и запуска бота выполните следующие шаги:

### Шаг 1: Клонирование репозитория

Склонируйте этот репозиторий на вашу локальную машину:

```sh
git clone https://github.com/Rachalovsky/TelegramBot.git
cd TelegramBot
```

POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DATABASE=postgres
POSTGRES_HOST=postgres_db
POSTGRES_PORT=5432

### Шаг 2: Создание и настройка `.env.docker` файла

Создайте файл `.env.docker` в корневой директории проекта и добавьте следующие переменные окружения:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@db:5432/postgres
```

### Шаг 3: Построение и запуск контейнеров Docker

```sh
docker-compose up -d
```
Вы должны увидеть контейнеры `postgres_db` и `bot_container` со статусом Up.

### Шаг 4: Проверка запуска

```sh
docker-compose ps
```
---
## Структура проекта
```
Bot/
├── src/
│   ├── config.py
│   └── main.py
│   ├── database/
│   │   ├── conn.py
│   │   ├── models.py
│   │   └── requests.py
│   ├── handlers/
│   │   ├── bot_commands.py
│   │   ├── menu.py
│   │   ├── registration.py
│   │   └── tasks.py
│   ├── tools/
│   │   ├── filters.py
│   │   ├── keyboards.py
│   │   └── other.py
├── .env.docker
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
```


