# Vacancy Hunter — Поиск вакансий с hh.ru

Проект для автоматического сбора данных о компаниях и вакансиях с сайта [hh.ru](https://hh.ru) и анализа через PostgreSQL.

## Описание

Приложение получает данные о 10+ компаниях и их вакансиях через публичное API hh.ru, сохраняет их в базу данных PostgreSQL и предоставляет удобный интерфейс для анализа:
- Количество вакансий у каждой компании
- Список всех вакансий с зарплатами
- Средняя зарплата по рынку
- Вакансии выше средней зарплаты
- Поиск по ключевым словам

## Технологии

- **Python 3.14**
- **PostgreSQL** — хранение данных
- **psycopg2** — работа с БД
- **requests** — запросы к API hh.ru
- **python-dotenv** — управление переменными окружения

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone <git@github.com:mossssolma-ui/project3_job_search_with_db_connection.git>
   cd project3_job_search_with_db_connection
2. Установите зависимости через Poetry:
   ```bash
   poetry install
3. Настройте переменные окружения:
   ```bash
    HOST=localhost
    PORT=5432
    DATABASE=postgres
    USER=your_username
    PASSWORD=your_password
4. Запустите приложение:
   ```bash
   python main.py
   
## Структура проекта 
```
project3_job_search_with_db_connection/
├── src/
├   └── project3_job_search_with_db_connection/
├       ├── __init__.py     
├       ├── hh_api.py       # Работа с API hh.ru (AbstractAPI + HeadHunterAPI)
├       ├── utils.py        # Вспомогательные функции (загрузка данных, работа с БД)
├       └── db_manager.py   # Класс DBManager для анализа данных
├        
├── main.py                 # Точка входа, интерфейс пользователя
├── pyproject.toml          # Зависимости и метаданные (Poetry)
├── poetry.toml             # Виртуальное окружение в проекте 
├── poetry.lock             # Фиксация версий зависимостей
├── .env.template           # Шаблон для .env
├── .flake8
├── .gitignore
├── README.md               # Описание проекта

```

## Примеры использования
```
---------------МЕНЮ---------------
1 - Компания и количество вакансий
2 - Все вакансии
3 - Средняя зарплата
4 - Вакансии выше средней зарплаты
5 - Поиск вакансий по ключевому слову
0 - Выход
```
### Пример поиска вакансий
```
Введите пункт меню: 5
Введите ключевые слова через пробел: python junior
Москва: Junior Python Developer: 120000.0: https://hh.ru/vacancy/12345678
Санкт-Петербург: Python-разработчик (junior): Зарплата не указана: https://hh.ru/vacancy/87654321
```