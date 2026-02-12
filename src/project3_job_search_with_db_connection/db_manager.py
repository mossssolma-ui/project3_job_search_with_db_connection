import html
import re
from typing import Any, Optional

import psycopg2
from psycopg2 import sql


class DBManager:
    """Класс для работы с БД PostgreSQL"""

    def __init__(self, db_name: str, params: dict) -> None:
        """Инициализация подключения к БД"""
        self.db_name = db_name
        self.params = params.copy()
        self.params["database"] = db_name
        self._conn = psycopg2.connect(**self.params)

    def close(self) -> None:
        """Закрывает соединение"""
        if self._conn and not self._conn.closed:
            self._conn.close()

    @staticmethod
    def create_database(db_name: str, params: dict) -> None:
        """Создание БД если её нет"""
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        try:
            with conn.cursor() as cur:
                cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), (db_name.lower(),))
                if not cur.fetchone():
                    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                    print(f"БД {db_name} успешно создана")
                else:
                    print(f"БД {db_name} уже существует")
        except Exception as e:
            print(f"Ошибка при создании БД: {e}")
        finally:
            conn.close()

    @staticmethod
    def clear_description(string: str) -> str:
        """Удаление спецсимволов из строки"""
        if not string:
            return ""
        string = re.sub(r"<.*?>", "", string)
        string = html.unescape(string)
        string = re.sub(r"\s+", " ", string).strip()
        return string

    def create_tables(self) -> None:
        """Создание таблиц companies и vacancies"""
        try:
            with self._conn.cursor() as cur:
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
                        salary INT,
                        url TEXT NOT NULL,

                        FOREIGN KEY(company_id) REFERENCES companies(company_id)
                    )
                """)

        except Exception as e:
            print(f"Произошла ошибка при создании таблиц: {e}")

    def truncate_tables(self) -> None:
        """Очистка таблиц companies и vacancies перед загрузкой"""
        try:
            with self._conn.cursor() as cur:
                cur.execute("TRUNCATE TABLE vacancies RESTART IDENTITY CASCADE;")
                cur.execute("TRUNCATE TABLE companies RESTART IDENTITY CASCADE;")
        except Exception as e:
            print(f"Произошла ошибка при очистке таблиц: {e}")

    def save_data_to_database(self, data: list[dict[str, Any]]) -> None:
        """Сохранение данных о работодателях и вакансиях в БД"""
        try:
            with self._conn.cursor():
                for company in data:
                    company_info = company["company"]
                    company_name = company_info.get("name", "Не указано")
                    company_city = company_info.get("area", {}).get("name", "Не указан")
                    company_description = self.clear_description(company_info.get("description", ""))
                    company_url = company_info.get("alternate_url", "")

                    company_query = """
                        INSERT INTO companies (name, city, description, url)
                        VALUES (%s, %s, %s, %s)
                        RETURNING company_id
                    """
                    result = self.execute_query(
                        company_query, (company_name, company_city, company_description, company_url), True
                    )
                    if not result:
                        print(f"Компания {company_name} не сохранена")
                        continue
                    company_id = result[0][0]

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

                        vacancy_query = """
                            INSERT INTO vacancies (company_id, city, name, salary, url)
                            VALUES (%s, %s, %s, %s, %s)
                            """
                        self.execute_query(
                            vacancy_query, (company_id, vacancy_city, vacancy_name, vacancy_salary, vacancy_url)
                        )

        except Exception as e:
            self._conn.rollback()
            print(f"Произошла ошибка при заполнении таблиц: {e}")

    def execute_query(self, query: str, params: Optional[tuple[Any, ...]] = None, fetch: bool = False) -> list[tuple]:
        """Выполнение запроса"""
        try:
            with self._conn.cursor() as cur:
                cur.execute(query, params)
                if fetch:
                    result = cur.fetchall()
                    self._conn.commit()
                    return result
                else:
                    self._conn.commit()
                    return []
        except Exception as e:
            self._conn.rollback()
            print(f"Ошибка при выполнении запроса {e}")
            return []

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Получает список всех компаний
        и количество вакансий у каждой компании. Отсортир
        """
        query = """SELECT c.name, v.vacancy_count
                    FROM companies AS c
                    INNER JOIN (
                        SELECT company_id, COUNT(*) AS vacancy_count
                        FROM vacancies
                        GROUP BY company_id
                    ) AS v ON c.company_id = v.company_id
                    ORDER BY v.vacancy_count DESC, c.name;
                """
        return self.execute_query(query, fetch=True)

    def get_all_vacancies(self) -> list[tuple]:
        """Получает список всех вакансий
        с указанием названия компании,
        названия вакансии и зарплаты
        и ссылки на вакансию.
        """
        query = """SELECT
                        c.name AS company_name,
                        v.name AS vacancy_name,
                        v.salary,
                        v.url
                    FROM vacancies AS v
                    INNER JOIN companies AS c ON c.company_id = v.company_id;
                """
        return self.execute_query(query, fetch=True)

    def get_avg_salary(self) -> list[tuple]:
        """Получает среднюю зарплату по вакансиям."""
        query = """SELECT avg(salary) as avg_salary
                   FROM vacancies
                   WHERE salary IS NOT NULL;
                """
        return self.execute_query(query, fetch=True)

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """Получает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям.
        """
        query = """SELECT name, salary, url FROM vacancies
                    WHERE salary > (
                        SELECT avg(salary) as avg_salary
                        FROM vacancies
                        WHERE salary IS NOT NULL
                        )
                    ORDER BY salary DESC;
                """
        return self.execute_query(query, fetch=True)

    def get_vacancies_with_keyword(self, keyword: list[str]) -> list:
        """
        Получает список всех вакансий,
        в названии которых содержатся
        переданные слова
        """
        if not keyword:
            return []

        placeholters = " OR ".join(["name ILIKE %s"] * len(keyword))

        query = """
            SELECT city, name, salary, url
            FROM vacancies
            WHERE {}
            ORDER BY name;
        """.format(placeholters)

        params = tuple(f"%{word}%" for word in keyword)

        return self.execute_query(query, params, fetch=True)
