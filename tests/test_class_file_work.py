import json
import pytest
import tempfile
import os
from unittest.mock import Mock
from src.class_abs_file_work import FileWorker
from src.class_vacancies import Vacancy
from src.class_file_work import JSONFileWorker


@pytest.fixture
def temp_file():
    """Фикстура для создания временного файла."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('[]')  # Создаем пустой JSON файл
        temp_path = f.name
    yield temp_path
    # Удаляем временный файл после теста
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def sample_vacancies():
    """Фикстура для создания тестовых вакансий."""
    vacancy1 = Mock(spec=Vacancy)
    vacancy1.alternate_url = "https://hh.ru/vacancy/1"
    vacancy1.to_dict.return_value = {
        "name": "Python Developer",
        "salary": 100000,
        "alternate_url": "https://hh.ru/vacancy/1",
        "employer": "Company A",
        "snippet": "Python experience",
        "experience": "1-3 years",
        "employment": "full"
    }

    vacancy2 = Mock(spec=Vacancy)
    vacancy2.alternate_url = "https://hh.ru/vacancy/2"
    vacancy2.to_dict.return_value = {
        "name": "Java Developer",
        "salary": 120000,
        "alternate_url": "https://hh.ru/vacancy/2",
        "employer": "Company B",
        "snippet": "Java experience",
        "experience": "3-5 years",
        "employment": "remote"
    }

    return [vacancy1, vacancy2]


class TestJSONFileWorker:
    """Тесты для класса JSONFileWorker."""

    def test_init_default_filename(self):
        """Тест инициализации с дефолтным именем файла."""
        worker = JSONFileWorker()
        # Проверяем, что __filename является приватным
        assert hasattr(worker, '_JSONFileWorker__filename')
        assert worker._JSONFileWorker__filename == "data/vacancy.json"

    def test_init_custom_filename(self):
        """Тест инициализации с кастомным именем файла."""
        worker = JSONFileWorker("custom.json")
        assert worker._JSONFileWorker__filename == "custom.json"

    def test_get_data_file_not_exists(self):
        """Тест получения данных из несуществующего файла."""
        worker = JSONFileWorker("non_existent.json")
        # Используем capsys для перехвата вывода print
        result = worker.get_data()
        assert result is None

    def test_get_data_valid_file(self, temp_file):
        """Тест получения данных из существующего файла."""
        # Записываем тестовые данные в файл
        test_data = [{"name": "Test", "salary": 50000}]
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)

        worker = JSONFileWorker(temp_file)
        result = worker.get_data()
        assert result == test_data

    def test_get_data_invalid_json(self, temp_file):
        """Тест получения данных из файла с некорректным JSON."""
        # Записываем некорректный JSON
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("{ invalid json ")

        worker = JSONFileWorker(temp_file)
        result = worker.get_data()
        assert result is None

    def test_load_data_to_empty_file(self, temp_file, sample_vacancies):
        """Тест загрузки данных в пустой файл."""
        worker = JSONFileWorker(temp_file)

        # Загружаем вакансии
        worker.load_data(sample_vacancies)

        # Читаем файл и проверяем
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert len(data) == 2
        assert data[0]["alternate_url"] == "https://hh.ru/vacancy/1"
        assert data[1]["alternate_url"] == "https://hh.ru/vacancy/2"

    def test_load_data_prevent_duplicates(self, temp_file, sample_vacancies):
        """Тест предотвращения дублирования при загрузке."""
        worker = JSONFileWorker(temp_file)

        # Первая загрузка
        worker.load_data(sample_vacancies)

        # Вторая загрузка тех же вакансий (дубликаты не должны добавиться)
        worker.load_data(sample_vacancies)

        # Читаем файл и проверяем
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Должно остаться только 2 уникальные вакансии
        assert len(data) == 2

    def test_load_data_add_new_vacancies(self, temp_file, sample_vacancies):
        """Тест добавления новых вакансий к существующим."""
        worker = JSONFileWorker(temp_file)

        # Загружаем первую вакансию
        worker.load_data([sample_vacancies[0]])

        # Создаем новую вакансию
        vacancy3 = Mock(spec=Vacancy)
        vacancy3.alternate_url = "https://hh.ru/vacancy/3"
        vacancy3.to_dict.return_value = {
            "name": "Go Developer",
            "salary": 140000,
            "alternate_url": "https://hh.ru/vacancy/3",
            "employer": "Company C",
            "snippet": "Go experience",
            "experience": "2-4 years",
            "employment": "hybrid"
        }

        # Загружаем новую вакансию
        worker.load_data([vacancy3])

        # Читаем файл и проверяем
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert len(data) == 2  # Должно быть 2 вакансии
        urls = {v["alternate_url"] for v in data}
        assert "https://hh.ru/vacancy/1" in urls
        assert "https://hh.ru/vacancy/3" in urls

    def test_delete_data_existing_url(self, temp_file, sample_vacancies):
        """Тест удаления данных по существующему URL."""
        worker = JSONFileWorker(temp_file)

        # Сначала загружаем данные
        worker.load_data(sample_vacancies)

        # Удаляем одну вакансию
        worker.delete_data("https://hh.ru/vacancy/1")

        # Проверяем, что осталась только одна вакансия
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["alternate_url"] == "https://hh.ru/vacancy/2"

    def test_delete_data_non_existing_url(self, temp_file, sample_vacancies):
        """Тест удаления по несуществующему URL."""
        worker = JSONFileWorker(temp_file)

        # Сначала загружаем данные
        worker.load_data(sample_vacancies)

        # Пытаемся удалить несуществующую вакансию
        initial_length = len(json.load(open(temp_file, 'r', encoding='utf-8')))
        worker.delete_data("https://hh.ru/vacancy/999")

        # Проверяем, что данные не изменились
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert len(data) == initial_length

    def test_delete_data_from_empty_file(self, temp_file):
        """Тест удаления из пустого файла."""
        worker = JSONFileWorker(temp_file)

        # Файл пустой, пытаемся удалить
        worker.delete_data("https://hh.ru/vacancy/1")

        # Проверяем, что файл остался пустым
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert data == []

    def test_file_not_found_on_delete(self):
        """Тест удаления из несуществующего файла."""
        worker = JSONFileWorker("non_existent.json")
        # Должен отработать без ошибок, только print сообщение
        worker.delete_data("https://hh.ru/vacancy/1")

    def test_inheritance(self):
        """Тест, что класс наследуется от FileWorker."""
        worker = JSONFileWorker()
        assert isinstance(worker, FileWorker)


# Дополнительные тесты для edge cases
class TestJSONFileWorkerEdgeCases:
    """Дополнительные тесты для граничных случаев."""

    def test_load_data_empty_list(self, temp_file):
        """Тест загрузки пустого списка вакансий."""
        worker = JSONFileWorker(temp_file)

        # Начальное состояние файла
        initial_data = []
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f)

        # Загружаем пустой список
        worker.load_data([])

        # Проверяем, что файл остался пустым
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert data == []

    def test_corrupted_file_recovery(self, temp_file):
        """Тест восстановления после поврежденного файла."""
        worker = JSONFileWorker(temp_file)

        # Создаем поврежденный JSON файл
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("{ invalid json")

        # Создаем mock вакансию
        vacancy = Mock(spec=Vacancy)
        vacancy.alternate_url = "https://hh.ru/vacancy/1"
        vacancy.to_dict.return_value = {"name": "Test", "alternate_url": "https://hh.ru/vacancy/1"}

        # Пытаемся загрузить данные - должен восстановиться
        worker.load_data([vacancy])

        # Проверяем, что файл теперь валидный
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["alternate_url"] == "https://hh.ru/vacancy/1"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
