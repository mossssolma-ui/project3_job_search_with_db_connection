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
- **tabulate** — отображение данных в ввиде таблицы
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
    DB_HOST=localhost
    DB_PORT=5432
    DB_DATABASE=postgres
    DB_USER=your_username
    DB_PASSWORD=your_password
4. Запустите приложение:
   ```bash
   python main.py
   
## Структура проекта 
```
project3_job_search_with_db_connection/
├── src/
├   └── project3_job_search_with_db_connection/
├       ├── __init__.py     
├       ├── hh_api.py       # Работа с API hh.ru
├       ├── utils.py        # Вспомогательные функции 
├       └── db_manager.py   # Класс DBManager для анализа данных (загрузка данных, работа с БД)
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
| city            | name                                                                 | salary     | url                             |
|-----------------|----------------------------------------------------------------------|------------|---------------------------------|
| Москва          | Expert IT Support Junior System Administrator                        | Не указана | https://hh.ru/vacancy/130297571 |
| Санкт-Петербург | Junior HR BP - Специалист по персоналу (DS)                          | Не указана | https://hh.ru/vacancy/130320238 |
| Москва          | Senior SDET Python (VM)                                              | Не указана | https://hh.ru/vacancy/130204934 |
| Москва          | Стажёр - инженер по тестированию Python, Склад                       | Не указана | https://hh.ru/vacancy/130221299 |
| Санкт-Петербург | Старший Python-разработчик в команду Кино/ТВ (Django Rest Framework) | Не указана | https://hh.ru/vacancy/130388278 |
```