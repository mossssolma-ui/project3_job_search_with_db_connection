from abc import ABC, abstractmethod
from typing import Any, Optional

import requests
from requests import Response


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def get_employer_vacancies(self, employer_id: str) -> list[dict]:
        """Абстрактный метод для получения вакансий работодателя"""
        ...

    @abstractmethod
    def get_employer_info(self, employer_id: str) -> dict:
        """Абстрактный метод для получения информации о работодателе"""
        ...


class HeadHunterAPI(AbstractAPI):
    """Класс для работы c API hh.ru"""

    def __init__(self, page: int = 0):
        """Инициалиализация подключения"""
        self._base_url = "https://api.hh.ru/"
        self._headers = {"User-Agent": "HH-User-Agent"}
        self._params = {"page": page, "per_page": 30}

    def _connect(self, end: str, params: Optional[dict[Any, Any]] = None) -> Response:
        """Метод для подключения к API"""
        url = f"{self._base_url}{end}"
        params_init = self._params.copy()
        if params:
            params_init.update(params)

        response = requests.get(url, headers=self._headers, params=params_init)
        response.raise_for_status()
        return response

    def get_employer_vacancies(self, employer_id: str) -> list[dict]:
        """Метод получения вакансий конкретного работодателя"""
        params = {"employer_id": employer_id}
        response = self._connect("vacancies", params)
        return response.json().get("items", [])  # type: ignore

    def get_employer_info(self, employer_id: str) -> dict:
        """Метод получения информации о работодателе"""
        end = f"employers/{employer_id}"
        response = self._connect(end, params={})
        return response.json()  # type: ignore
