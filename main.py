import json

from src.project3_job_search_with_db_connection.hh_api import HeadHunterAPI


def user_vacancies() -> None:
    """Основная функция взаимодействия с пользователем через консоль."""
    print("Добро пожаловать в систему поиска вакансий!\n")

    # 1. Запрос у пользователя
    search_query = input("Введите поисковый запрос (например, 'Python разработчик'): ").strip()
    if not search_query:
        print("Поисковый запрос не может быть пустым.")
        return

    # 2. Получение вакансий с hh.ru в формате JSON
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies(search_query)

    if not hh_vacancies:
        print("По вашему запросу ничего не найдено.")
        return
    else:
        with open("data/hh_vacancies.json", "w", encoding="utf-8") as f:
            json.dump(hh_vacancies, f, ensure_ascii=False, indent=4)


def user_employer_vacancies() -> None:
    hh_api = HeadHunterAPI()

    companies = [
        "1455",  # hh.ru
        "1740",  # Яндекс
        "3529",  # Сбер
        "15478",  # VK
        "78638",  # Тинькофф
        "3388",  # Газпромбанк
        "907345",  # Лукойл
        "1057",  # Лаборатория Касперского
        "87021",  # Wildberries
        "2180",  # OZON
    ]

    all_data = {}

    successful_companies = 0
    total_vacancies = 0

    for company_id in companies:
        try:
            print(f"\nID компании : {company_id}")

            employer_info = hh_api.get_employer_info(company_id)

            company_name = employer_info.get("name", "Unknown")
            print(f"Название: {company_name}")

            vacancies = hh_api.get_employer_vacancies(company_id)

            all_data[company_id] = {"employer": employer_info, "vacancies": vacancies}

            successful_companies += 1
            total_vacancies += len(vacancies)
            print(f"Вакансий: {len(vacancies)}")

        except Exception as e:
            print(f"Ошибка: {e}")

    print(f"\n{'=' * 20}")
    print("ИТОГО:")
    print(f"Успешно обработано: {successful_companies} из {len(companies)} компаний")
    print(f"Всего вакансий: {total_vacancies}")


def main() -> None:
    user_vacancies()
    user_employer_vacancies()


if __name__ == "__main__":
    main()
