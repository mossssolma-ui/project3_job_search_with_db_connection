from abc import ABC, abstractmethod
from typing import Any, Optional

from requests import Response


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def _connect(self, end: str, params: Optional[dict[Any, Any]] = None) -> Response:
        """Абстрактный метод для подключения к API"""
        ...

    @abstractmethod
    def get_vacancies(self, query: str) -> list[dict]:
        """Абстрактный метод для получения вакансий по запросу"""
        ...

    @abstractmethod
    def get_employer_vacancies(self, employer_id: str) -> list[dict]:
        """Абстрактный метод для получения вакансий работодателя"""
        ...

    @abstractmethod
    def get_employer_info(self, employer_id: str) -> dict:
        """Абстрактный метод для получения информации о работодателе"""
        ...
