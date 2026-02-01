from unittest.mock import Mock, patch

from src.project3_job_search_with_db_connection.hh_api import HeadHunterAPI as HH


def test_hh_api_init() -> None:
    """Тест инициализации"""
    hh_api = HH()
    assert hh_api._base_url == "https://api.hh.ru/"
    assert hh_api._headers == {"User-Agent": "HH-User-Agent"}
    assert hh_api._params == {"page": 0, "per_page": 30}


@patch("src.project3_job_search_with_db_connection.hh_api.requests.get")
def test_get_vacancies(mock_get: Mock, vacancies_response: dict) -> None:
    """Тест успешного получения вакансии по запросу"""
    mock_get.return_value = vacancies_response
    hh_api = HH()
    vacancies = hh_api.get_vacancies("Python")

    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Python-разработчик"
    assert vacancies[0]["id"] == "130039123"
    assert vacancies[0]["salary"]["from"] == 85000

    mock_get.assert_called_once()
    call_args = mock_get.call_args

    assert "vacancies" in call_args[0][0]
    params = call_args[1]["params"]
    assert params["page"] == 0
    assert params["per_page"] == 30
    assert params["text"] == "Python"


@patch("src.project3_job_search_with_db_connection.hh_api.requests.get")
def test_get_employer_info(mock_get: Mock, employer_response: dict) -> None:
    """Тест успешного полученияя информации о работодателе"""
    mock_get.return_value = employer_response
    hh_api = HH()
    employer_info = hh_api.get_employer_info("1740")

    assert employer_info["id"] == "1740"
    assert employer_info["name"] == "Яндекс"
    assert employer_info["open_vacancies"] == 742
    assert employer_info["site_url"] == "https://yandex.ru/jobs/"

    call_args = mock_get.call_args
    assert "employers/1740" in call_args[0][0]


@patch("src.project3_job_search_with_db_connection.hh_api.requests.get")
def test_get_vacancies_empty(mock_get: Mock, empty_response: dict) -> None:
    """Тест получения пустого списка вакансий"""
    mock_get.return_value = empty_response

    hh_api = HH()
    vacancies = hh_api.get_vacancies("несуществующий запрос")

    assert vacancies == []
    assert len(vacancies) == 0


@patch("src.project3_job_search_with_db_connection.hh_api.requests.get")
def test_get_employer_vacancies(mock_get: Mock, vacancies_response: dict) -> None:
    """Тест успешного получения вакансии конкретного работодателя"""
    mock_get.return_value = vacancies_response
    hh_api = HH()
    vacancies = hh_api.get_employer_vacancies("1740")

    assert len(vacancies) == 1
    assert vacancies[0]["id"] == "130039123"
    assert vacancies[0]["name"] == "Python-разработчик"
    assert vacancies[0]["salary"]["from"] == 85000
    assert vacancies[0]["employer"]["id"] == "1740"
    assert vacancies[0]["employer"]["name"] == "Яндекс"
