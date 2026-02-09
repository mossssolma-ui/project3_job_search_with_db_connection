import os

from dotenv import load_dotenv

from src.project3_job_search_with_db_connection.db_manager import DBManager
from src.project3_job_search_with_db_connection.utils import (
    create_database,
    create_tables,
    get_company_vacancy,
    save_data_to_database,
    truncate_tables,
)

load_dotenv()


def main() -> None:
    companies = [
        "1122462",  # Skyeng
        "1740",  # Яндекс
        "3529",  # Сбер
        "15478",  # VK
        "78638",  # Тинькофф
        "4412077",  # Табачная компания ПЕППЕЛЛ
        "907345",  # Лукойл
        "1057",  # Лаборатория Касперского
        "87021",  # Wildberries
        "2180",  # OZON
    ]
    params = {
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT"),
        "database": os.getenv("DATABASE"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
    }

    db_name = "vacancy_hunter"

    data = get_company_vacancy(companies)
    create_database(db_name, params)
    create_tables(db_name, params)
    truncate_tables(db_name, params)
    save_data_to_database(data, db_name, params)
    db = DBManager(db_name, params)

    while True:
        print(f"\n{'-' * 15}МЕНЮ{'-' * 15}")
        print("1 - Компания и количество вакансий")
        print("2 - Все вакансии")
        print("3 - Средняя зарплата")
        print("4 - Вакансии выше средней зарплаты")
        print("5 - Поиск вакансий по ключевому слову")
        print("0 - Выход\n")

        user_choice = input("Введите пункт меню: ").strip()

        if user_choice == "1":
            for name, count in db.get_companies_and_vacancies_count():
                print(f"{name}: {count}")

        elif user_choice == "2":
            for company, vacancy, salary, url in db.get_all_vacancies():
                if salary is None:
                    salary = "Зарплата не указана"
                print(f"{company}: {vacancy}: {salary}: {url}")

        elif user_choice == "3":
            result = db.get_avg_salary()
            if result and result[0][0] is not None:
                avg_salary = round(result[0][0], 2)
                print(f"Средняя зарплата: {avg_salary}")
            else:
                print("Нет данных для вычисления средней зарплаты")

        elif user_choice == "4":
            for vacancy, salary, url in db.get_vacancies_with_higher_salary():
                print(f"{vacancy}: {salary}: {url}")

        elif user_choice == "5":
            print("Введите ключевые слова через пробел: ", end=" ")
            user_keywords = input().split()
            for city, name, salary, url in db.get_vacancies_with_keyword(user_keywords):
                if salary is None:
                    salary = "Зарплата не указана"
                print(f"{city}: {name}: {salary}: {url}")

        elif user_choice == "0":
            print("Ну что ж, до скорой встречи :D")
            break

        else:
            print("\nТакая команда отсутствует. Повторите ввод")


if __name__ == "__main__":
    main()
