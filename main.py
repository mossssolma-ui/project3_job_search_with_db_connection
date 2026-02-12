import os

from dotenv import load_dotenv
from tabulate import tabulate

from project3_job_search_with_db_connection.db_manager import DBManager
from project3_job_search_with_db_connection.utils import get_company_vacancy

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
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "database": os.getenv("DB_DATABASE"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }

    db_name = "vacan"

    print("Загружаю данные с hh.ru...")
    data = get_company_vacancy(companies)

    print(f"Создаю БД {db_name}")
    DBManager.create_database(db_name, params)

    db = DBManager(db_name, params)

    print("Работаю над созданием таблиц")
    db.create_tables()
    db.truncate_tables()

    print("Заполняю таблицы")
    db.save_data_to_database(data)

    print("Данные готовы для использования")

    while True:
        print(f"\n{'-' * 15}МЕНЮ{'-' * 15}")
        print("1 - Компании и количество вакансий")
        print("2 - Все вакансии")
        print("3 - Средняя зарплата")
        print("4 - Вакансии выше средней зарплаты")
        print("5 - Поиск вакансий по ключевому слову")
        print("0 - Выход\n")

        user_choice = input("Введите пункт меню: ").strip()

        result = []
        hds = []

        if user_choice == "1":
            hds = ["company", "count"]
            for data in db.get_companies_and_vacancies_count():
                result.append(data)

        elif user_choice == "2":
            hds = ["company", "vacancy", "salary", "url"]
            for data in db.get_all_vacancies():
                company, vacancy, salary, url = data
                if salary is None:
                    salary = "Не указана"
                result.append((company, vacancy, salary, url))

        elif user_choice == "3":
            hds = ["avg_salary"]
            data = db.get_avg_salary()
            if data and data[0][0] is not None:
                avg_salary = round(data[0][0], 2)
                result.append((f"{avg_salary} руб.",))
            else:
                result.append(("Нет данных для расчета",))

        elif user_choice == "4":
            hds = ["vacancy", "salary", "url"]
            for data in db.get_vacancies_with_higher_salary():
                vacancy, salary, url = data
                if salary is None:
                    salary = "Не указана"
                result.append((vacancy, salary, url))

        elif user_choice == "5":
            print("Введите ключевые слова через пробел: ", end=" ")
            user_keywords = input().split()
            hds = ["city", "name", "salary", "url"]
            for data in db.get_vacancies_with_keyword(user_keywords):
                city, name, salary, url = data
                if salary is None:
                    salary = "Не указана"
                result.append((city, name, salary, url))

        elif user_choice == "0":
            print("Ну что ж, до скорой встречи :D")
            break

        else:
            print("\nТакая команда отсутствует. Повторите ввод")
            continue

        print("Обработка...")
        print(f"Получено строк: {len(result)}")
        print("Вывод:")

        if result:
            print(tabulate(result, headers=hds, tablefmt="github"))
        else:
            print("Нет данных для отображения")

    db.close()


if __name__ == "__main__":
    main()
