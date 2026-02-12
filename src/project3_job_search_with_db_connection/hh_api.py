from typing import Any, Optional

import requests
from requests import Response


class HeadHunterAPI:
    """Класс для работы c API hh.ru"""

    def __init__(self) -> None:
        """Инициалиализация подключения"""
        self._base_url = "https://api.hh.ru/"
        self._headers = {"User-Agent": "HH-User-Agent"}

    def _get(self, end: str, params: Optional[dict[Any, Any]] = None) -> Response:
        """Выполняет GET-запрос и возвращает ответ"""
        url = f"{self._base_url}{end}"
        response = requests.get(url, headers=self._headers, params=params)
        response.raise_for_status()
        return response

    def get_employer_vacancies(self, employer_id: str, page: int = 0, per_page: int = 30) -> list[dict]:
        """Метод получения вакансий конкретного работодателя"""
        params = {"employer_id": employer_id, "page": page, "per_page": per_page}
        response = self._get("vacancies", params)
        return response.json().get("items", [])

    def get_employer_info(self, employer_id: str) -> dict:
        """Метод получения информации о работодателе"""
        end = f"employers/{employer_id}"
        response = self._get(end)
        return response.json()
