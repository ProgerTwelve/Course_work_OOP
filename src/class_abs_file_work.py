from abc import ABC, abstractmethod

class FileWorker(ABC):
    """Абстрактный класс для работы с файлами. Является родительским для
    класса JSONFileWorker."""

    @abstractmethod
    def __init__(self):
        """Конструктор класса"""

        pass

    @abstractmethod
    def get_data(self):
        """Абстрактный метод получения данных из файла."""

        pass

    @abstractmethod
    def load_data(self, *args, **kwargs):
        """Абстрактный метод добавления данных в файл."""

        pass

    @abstractmethod
    def delete_data(self, *args, **kwargs):
        """Абстрактный метод удаления данных из файла."""

        pass
