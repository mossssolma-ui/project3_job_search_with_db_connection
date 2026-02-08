import html
import re
from typing import Any

import psycopg2

from src.project3_job_search_with_db_connection.hh_api import HeadHunterAPI


def get_company_vacancy(companies: list[str]) -> list[dict[str, Any]]:
    """Получение данных о работодателях и их вакансиях"""
    hh_api = HeadHunterAPI()
    data = []
    for company in companies:
        company_data = hh_api.get_employer_info(company)
        all_vacancy = hh_api.get_employer_vacancies(company_data["id"])

        if not all_vacancy:
            print(f"Не удалось получить вакансии для id компании : {company}")
            all_vacancy = []

        data.append({"company": company_data, "vacancy": all_vacancy})

    return data


def create_database(db_name: str, params: dict) -> None:
    """Создание БД если ее нет"""

    conn = psycopg2.connect(**params)
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
            exists = cur.fetchone() is not None
            if not exists:
                cur.execute(f"CREATE DATABASE {db_name};")
    except Exception as e:
        print(f"Произошла ошибка при создании БД: {e}")
    finally:
        conn.close()


def create_tables(db_name: str, params: dict) -> None:
    """Создание таблиц companies и vacancies"""
    params = params.copy()
    params["database"] = db_name

    conn = psycopg2.connect(**params)
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS companies(
                    company_id SERIAL PRIMARY KEY,
                    hh_id int UNIQUE,
                    name VARCHAR(255) NOT NULL,
                    city VARCHAR(100),
                    description TEXT,
                    url TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies(
                    vacancy_id SERIAL PRIMARY KEY,
                    hh_vacancy_id INT UNIQUE,
                    company_id INT,
                    city VARCHAR(100),
                    name VARCHAR(255) NOT NULL,
                    salary_min INT,
                    salary_max INT,
                    url TEXT NOT NULL,

                    FOREIGN KEY(company_id) REFERENCES companies(company_id)
                )
            """)
    except Exception as e:
        print(f"Произошла ошибка при создании таблиц: {e}")
    finally:
        conn.close()


def clear_description(string: str) -> str:
    """Полная очистка: теги + сущности + нормализация пробелов"""
    if not string:
        return ""
    string = re.sub(r"<.*?>", "", string)
    string = html.unescape(string)
    string = re.sub(r"\s+", " ", string).strip()
    return string


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных о работодателях и вакансиях в БД"""
    params = params.copy()
    params["database"] = database_name

    conn = psycopg2.connect(**params)
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            for company in data:
                company_info = company["company"]
                company_hh_id = company_info["id"]
                company_name = company_info.get("name", "Не указано")
                company_city = company_info.get("area", {}).get("name", "Не указан")
                company_description = clear_description(company_info.get("description", ""))
                company_url = company_info.get("alternate_url", "")

                cur.execute(
                    """
                    INSERT INTO companies (hh_id, name, city, description, url)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (hh_id) DO UPDATE SET
                        name = EXCLUDED.name,
                        city = EXCLUDED.city,
                        description = EXCLUDED.description,
                        url = EXCLUDED.url
                    RETURNING company_id
                    """,
                    (company_hh_id, company_name, company_city, company_description, company_url),
                )
                company_id = cur.fetchone()[0]
                vacancy_data = company["vacancy"]
                for vacancy in vacancy_data:
                    vacancy_id = vacancy["id"]
                    vacancy_name = vacancy.get("name", "Без названия")
                    vacancy_city = vacancy.get("area", {}).get("name", "Не указан")
                    vacancy_url = vacancy.get("alternate_url", "")

                    salary = vacancy.get("salary", 0)
                    vacancy_min = salary.get("from") if salary and salary.get("from") is not None else 0
                    vacancy_max = salary.get("to") if salary and salary.get("to") is not None else 0

                    cur.execute(
                        """
                        INSERT INTO vacancies (hh_vacancy_id, company_id, city, name, salary_min, salary_max, url)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (hh_vacancy_id) DO NOTHING
                        """,
                        (vacancy_id, company_id, vacancy_city, vacancy_name, vacancy_min, vacancy_max, vacancy_url),
                    )
    except Exception as e:
        print(f"Произошла ошибка при заполнении таблиц: {e}")
    finally:
        conn.close()
