import os

from dotenv import load_dotenv

from src.project3_job_search_with_db_connection.utils import (
    get_company_vacancy,
    create_database,
    save_data_to_database,
    create_tables,
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
    db_name = "vacancy_test"
    params = {
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT"),
        "database": os.getenv("DATABASE"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
    }

    data = get_company_vacancy(companies)
    create_database(db_name, params)
    create_tables(db_name, params)
    save_data_to_database(data, db_name, params)


if __name__ == "__main__":
    main()
