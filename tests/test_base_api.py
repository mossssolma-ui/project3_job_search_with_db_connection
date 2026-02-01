from abc import ABC

from src.project3_job_search_with_db_connection.base_api import AbstractAPI


def test_abstract_api() -> None:
    """Проверка что AbstractAPI наследуется от ABC"""
    assert issubclass(AbstractAPI, ABC)
