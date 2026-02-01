from unittest.mock import Mock

import pytest


@pytest.fixture
def vacancies_response() -> dict:
    """Фикстура для мокового ответа API с вакансиями"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "items": [
            {
                "id": "130039123",
                "name": "Python-разработчик",
                "salary": {
                    "from": 85000,
                    "to": 160000,
                    "currency": "RUB",
                },
                "employer": {"id": "1740", "name": "Яндекс", "url": "https://api.hh.ru/employers/1740"},
                "snippet": {
                    "requirement": "владеете грамотной устной и письменной речью на казахском и русском языках",
                    "responsibility": "осуществлять проверку и аудит кухонь по чек-листам",
                },
                "experience": {"id": "between1And3", "name": "От 1 года до 3 лет"},
                "employment": {"id": "full", "name": "Полная занятость"},
            }
        ],
        "found": 1,
        "pages": 1,
    }
    mock_response.raise_for_status = Mock()
    return mock_response


@pytest.fixture
def employer_response() -> dict:
    """Фикстура для мокового ответа API с работодателем"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": "1740",
        "name": "Яндекс",
        "type": "company",
        "description": "Будет сложно, будет интересно...",
        "site_url": "https://yandex.ru/jobs/",
        "alternate_url": "https://hh.ru/employer/1740",
        "vacancies_url": "https://api.hh.ru/vacancies?employer_id=1740",
        "logo_urls": {
            "original": "https://img.hhcdn.ru/employer-logo-original-round/3790846.png",
        },
        "area": {"id": "1", "name": "Москва"},
        "open_vacancies": 742,
    }
    mock_response.raise_for_status = Mock()
    return mock_response


@pytest.fixture
def empty_response() -> dict:
    """Пустой ответ"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [], "found": 0, "pages": 0}
    mock_response.raise_for_status = Mock()
    return mock_response
