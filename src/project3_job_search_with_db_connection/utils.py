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
                    name VARCHAR(255) NOT NULL,
                    city VARCHAR(100),
                    description TEXT,
                    url TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies(
                    vacancy_id SERIAL PRIMARY KEY,
                    company_id INT,
                    city VARCHAR(100),
                    name VARCHAR(255) NOT NULL,
                    salary FLOAT,
                    url TEXT NOT NULL,

                    FOREIGN KEY(company_id) REFERENCES companies(company_id)
                )
            """)
    except Exception as e:
        print(f"Произошла ошибка при создании таблиц: {e}")
    finally:
        conn.close()


def truncate_tables(db_name: str, params: dict) -> None:
    """Очистка таблиц companies и vacancies перед загрузкой"""
    params = params.copy()
    params["database"] = db_name

    conn = psycopg2.connect(**params)
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE vacancies RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE TABLE companies RESTART IDENTITY CASCADE;")
    except Exception as e:
        print(f"Произошла ошибка при очистке таблиц: {e}")
    finally:
        conn.close()


def clear_description(string: str) -> str:
    """Удаление спецсимволов из строки"""
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
                company_name = company_info.get("name", "Не указано")
                company_city = company_info.get("area", {}).get("name", "Не указан")
                company_description = clear_description(company_info.get("description", ""))
                company_url = company_info.get("alternate_url", "")

                cur.execute(
                    """
                    INSERT INTO companies (name, city, description, url)
                    VALUES (%s, %s, %s, %s)
                    RETURNING company_id
                    """,
                    (company_name, company_city, company_description, company_url),
                )
                company_id = cur.fetchone()[0]
                vacancy_data = company["vacancy"]
                for vacancy in vacancy_data:
                    vacancy_name = vacancy.get("name", "Без названия")
                    vacancy_city = vacancy.get("area", {}).get("name", "Не указан")
                    vacancy_url = vacancy.get("alternate_url", "")

                    salary = vacancy.get("salary")
                    vacancy_salary = None

                    if salary:
                        from_salary = salary.get("from")
                        to_salary = salary.get("to")
                        if from_salary and from_salary > 0:
                            vacancy_salary = from_salary
                        elif to_salary and to_salary > 0:
                            vacancy_salary = to_salary

                    cur.execute(
                        """
                        INSERT INTO vacancies (company_id, city, name, salary, url)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (company_id, vacancy_city, vacancy_name, vacancy_salary, vacancy_url),
                    )
    except Exception as e:
        print(f"Произошла ошибка при заполнении таблиц: {e}")
    finally:
        conn.close()
