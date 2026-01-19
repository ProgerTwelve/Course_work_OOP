from abc import ABC, abstractmethod

class Parser(ABC):
    """Родительский класс для класса HH, в котором реализованы абстрактные методы."""

    @abstractmethod
    def __init__(self):
        """Конструктор класса."""

        pass

    @abstractmethod
    def _get_connection(self):
        """Абстрактный метод для подключения к API"""

        pass

    @abstractmethod
    def load_vacancies(self, *args, **kwargs):
        """Абстрактный метод загрузки вакансий."""

        pass
