import psycopg2


class DBManager:
    """Класс для работы с БД PostgreSQL"""

    def __init__(self, db_name: str, params: dict) -> None:
        """Инициализация подключения к БД"""
        self.params = params.copy()
        self.params["database"] = db_name
        self._conn = None

    def connect(self) -> None:
        """Подключение к БД"""
        if not self._conn or self._conn.closed:
            self._conn = psycopg2.connect(**self.params)

    def disconnect(self) -> None:
        """Отключение БД"""
        if self._conn and not self._conn.closed:
            self._conn.close()

    def run_query(self, query: str, params: tuple = None) -> list:  # type: ignore
        """Выполнение запроса"""
        self.connect()
        try:
            with self._conn.cursor() as cur:  # type: ignore
                cur.execute(query, params)
                result = cur.fetchall()
                return result  # type: ignore
        except Exception as e:
            print(f"Ошибка при выполнении запроса {e}")
        finally:
            self.disconnect()

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
        return self.run_query(query)

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
        return self.run_query(query)

    def get_avg_salary(self) -> list[tuple]:
        """Получает среднюю зарплату по вакансиям."""
        query = """SELECT avg(salary) as avg_salary
                   FROM vacancies
                   WHERE salary IS NOT NULL;
                """
        return self.run_query(query)

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
                """
        return self.run_query(query)

    def get_vacancies_with_keyword(self, keyword: list[str]) -> list:
        """Получает список всех вакансий,
        в названии которых содержатся
        переданные в метод слова
        """
        if not keyword:
            return []

        conditions = " OR ".join(["name ILIKE %s"] * len(keyword))
        params = [f"%{word}%" for word in keyword]

        query = f"""
                SELECT *
                FROM vacancies
                WHERE {conditions}
                ORDER BY name;
            """

        return self.run_query(query, tuple(params))
