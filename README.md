# VKParser_Telegram
Бот для автоматического парсинга новых постов с не ограниченного количества VK групп.

# Инструкция запуска бота:
1. Переменуйте файл `alembic.example.ini` и `config.example.ini` на `alembic.ini` и `config.ini`
2. Отредактируйте настройки в файле `config.ini`
3. Отредактируйте параметр `sqlalchemy.url` в файле `alembic.ini`
4. Проведите миграцию базы данных через команду `alembic upgrade head`
5. Всё готово к работе, можете запускать бота через файл `run.py`
