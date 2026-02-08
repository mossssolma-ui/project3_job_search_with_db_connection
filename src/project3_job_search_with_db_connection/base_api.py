from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API"""

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
