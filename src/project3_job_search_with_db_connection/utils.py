from typing import Any

from project3_job_search_with_db_connection.hh_api import HeadHunterAPI


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
