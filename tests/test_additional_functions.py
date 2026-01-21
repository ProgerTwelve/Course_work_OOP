import pytest
from unittest.mock import Mock

from src.additional_functions import (check_currency, vacancy_objects, filter_vacancies,
                                      get_vacancies_by_salary, sort_vacancies, get_top_vacancies)
from src.class_API import HH
from src.class_vacancies import Vacancy


class TestCheckCurrency:
    """Тесты для функции check_currency"""

    def test_check_currency_filters_rur_only(self):
        """Тест фильтрации только RUR валюты"""
        # Создаем мок-объект HH
        hh_mock = Mock(spec=HH)

        # Настраиваем данные с разными валютами
        hh_mock.vacancies = [
            {"name": "Python Dev", "salary": {"currency": "RUR", "from": 100000, "to": 150000}},
            {"name": "Java Dev", "salary": {"currency": "USD", "from": 2000, "to": 3000}},
            {"name": "Go Dev", "salary": {"currency": "RUR", "from": 120000, "to": 180000}},
            {"name": "JS Dev", "salary": {"currency": "EUR", "from": 3000, "to": 4000}},
            {"name": "C++ Dev", "salary": {"currency": "RUR", "from": 90000, "to": None}},
        ]

        # Вызываем функцию
        result = check_currency(hh_mock)

        # Проверяем результат
        assert len(result) == 3  # Только 3 вакансии с RUR
        assert all(v["salary"]["currency"] == "RUR" for v in result)
        assert result[0]["name"] == "Python Dev"
        assert result[1]["name"] == "Go Dev"
        assert result[2]["name"] == "C++ Dev"

    def test_check_currency_empty_result(self):
        """Тест, когда нет вакансий с RUR"""
        hh_mock = Mock(spec=HH)
        hh_mock.vacancies = [
            {"name": "Java Dev", "salary": {"currency": "USD", "from": 2000, "to": 3000}},
            {"name": "JS Dev", "salary": {"currency": "EUR", "from": 3000, "to": 4000}},
        ]

        result = check_currency(hh_mock)
        assert result == []  # Должен вернуться пустой список


class TestVacancyObjects:
    """Тесты для функции vacancy_objects"""

    def test_vacancy_objects_creation(self):
        """Тест создания объектов Vacancy из данных API"""
        # Тестовые данные из API
        vacancy_data = [
            {
                "name": "Python Developer",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "alternate_url": "https://hh.ru/vacancy/1",
                "employer": {"name": "Company A", "id": "123"},
                "snippet": {"requirement": "Python, Django"},
                "experience": {"name": "1-3 years"},
                "employment": {"name": "full"}
            },
            {
                "name": "Java Developer",
                "salary": {"from": 120000, "to": None, "currency": "RUR"},
                "alternate_url": "https://hh.ru/vacancy/2",
                "employer": {"name": "Company B", "id": "456"},
                "snippet": {"requirement": "Java, Spring"},
                "experience": {"name": "3-6 years"},
                "employment": {"name": "remote"}
            }
        ]

        # Вызываем функцию
        result = vacancy_objects(vacancy_data)

        # Проверяем результат
        assert len(result) == 2
        assert isinstance(result[0], Vacancy)
        assert isinstance(result[1], Vacancy)
        assert result[0].name == "Python Developer"
        assert result[0].alternate_url == "https://hh.ru/vacancy/1"
        assert result[1].name == "Java Developer"
        assert result[1].employer == "Company B"

    def test_vacancy_objects_empty_input(self):
        """Тест с пустым списком на входе"""
        result = vacancy_objects([])
        assert result == []


class TestFilterVacancies:
    """Тесты для функции filter_vacancies"""

    def test_filter_vacancies_by_keywords(self):
        """Тест фильтрации вакансий по ключевым словам"""
        # Создаем мок-объекты Vacancy
        vacancy1 = Mock(spec=Vacancy)
        vacancy1.name = "Senior Python Developer"

        vacancy2 = Mock(spec=Vacancy)
        vacancy2.name = "Java Backend Developer"

        vacancy3 = Mock(spec=Vacancy)
        vacancy3.name = "JavaScript Frontend Developer"

        vacancy4 = Mock(spec=Vacancy)
        vacancy4.name = "Python Data Scientist"

        vacancies = [vacancy1, vacancy2, vacancy3, vacancy4]

        # Фильтруем по ключевым словам
        keywords = ["python", "data"]
        result = filter_vacancies(vacancies, keywords)

        # Проверяем результат
        assert len(result) == 2
        assert vacancy1 in result  # Содержит "Python"
        assert vacancy4 in result  # Содержит "Python" и "Data"
        assert vacancy2 not in result
        assert vacancy3 not in result

    def test_filter_vacancies_case_insensitive(self):
        """Тест, что фильтрация нечувствительна к регистру"""
        vacancy1 = Mock(spec=Vacancy)
        vacancy1.name = "PYTHON Developer"

        vacancy2 = Mock(spec=Vacancy)
        vacancy2.name = "python backend"

        vacancy3 = Mock(spec=Vacancy)
        vacancy3.name = "Java Developer"

        vacancies = [vacancy1, vacancy2, vacancy3]

        # Ищем в нижнем регистре
        result = filter_vacancies(vacancies, ["python"])
        assert len(result) == 2
        assert vacancy1 in result
        assert vacancy2 in result

        # Ищем в верхнем регистре
        result = filter_vacancies(vacancies, ["PYTHON"])
        assert len(result) == 2


class TestGetVacanciesBySalary:
    """Тесты для функции get_vacancies_by_salary"""

    def test_get_vacancies_by_salary_range(self):
        """Тест фильтрации вакансий по диапазону зарплат"""
        # Создаем мок-объекты Vacancy с разными зарплатами
        vacancy1 = Mock(spec=Vacancy)
        vacancy1.salary = 80000

        vacancy2 = Mock(spec=Vacancy)
        vacancy2.salary = 120000

        vacancy3 = Mock(spec=Vacancy)
        vacancy3.salary = 150000

        vacancy4 = Mock(spec=Vacancy)
        vacancy4.salary = 200000

        vacancies = [vacancy1, vacancy2, vacancy3, vacancy4]

        # Фильтруем по диапазону 100000-180000
        salary_range = ["100000", "180000"]
        result = get_vacancies_by_salary(vacancies, salary_range)

        # Проверяем результат
        assert len(result) == 2
        assert vacancy2 in result  # 120000 в диапазоне
        assert vacancy3 in result  # 150000 в диапазоне
        assert vacancy1 not in result  # 80000 ниже диапазона
        assert vacancy4 not in result  # 200000 выше диапазона

    def test_get_vacancies_by_salary_edge_cases(self):
        """Тест граничных значений диапазона зарплат"""
        vacancy1 = Mock(spec=Vacancy)
        vacancy1.salary = 100000

        vacancy2 = Mock(spec=Vacancy)
        vacancy2.salary = 150000

        vacancy3 = Mock(spec=Vacancy)
        vacancy3.salary = 200000

        vacancies = [vacancy1, vacancy2, vacancy3]

        # Диапазон от 100000 до 200000 (включительно)
        salary_range = ["100000", "200000"]
        result = get_vacancies_by_salary(vacancies, salary_range)

        assert len(result) == 3  # Все три вакансии в диапазоне


class TestSortVacancies:
    """Тесты для функции sort_vacancies"""

    def test_sort_vacancies_descending(self):
        """Тест сортировки вакансий по убыванию зарплаты"""
        # Создаем мок-объекты с разными зарплатами
        vacancy1 = Mock(spec=Vacancy)
        vacancy1.salary = 80000

        vacancy2 = Mock(spec=Vacancy)
        vacancy2.salary = 120000

        vacancy3 = Mock(spec=Vacancy)
        vacancy3.salary = 100000

        vacancy4 = Mock(spec=Vacancy)
        vacancy4.salary = 150000

        vacancies = [vacancy1, vacancy2, vacancy3, vacancy4]

        # Сортируем
        result = sort_vacancies(vacancies)

        # Проверяем, что отсортированы по убыванию
        assert len(result) == 4
        assert result[0].salary == 150000
        assert result[1].salary == 120000
        assert result[2].salary == 100000
        assert result[3].salary == 80000

    def test_sort_vacancies_empty_list(self):
        """Тест сортировки пустого списка"""
        result = sort_vacancies([])
        assert result == []


class TestGetTopVacancies:
    """Тесты для функции get_top_vacancies"""

    def test_get_top_vacancies(self):
        """Тест получения топ N вакансий"""
        # Создаем мок-объекты с зарплатами
        vacancies = []
        for i in range(10):
            vacancy = Mock(spec=Vacancy)
            vacancy.salary = 100000 + i * 10000  # 100000, 110000, ..., 190000
            vacancies.append(vacancy)

        # Получаем топ 5 вакансий
        result = get_top_vacancies(vacancies, 5)

        # Проверяем результат
        assert len(result) == 5
        # Должны быть вакансии с самыми высокими зарплатами
        assert result[0].salary == 190000
        assert result[1].salary == 180000
        assert result[2].salary == 170000
        assert result[3].salary == 160000
        assert result[4].salary == 150000

    def test_get_top_vacancies_more_than_available(self):
        """Тест, когда запрашивают больше вакансий, чем есть"""
        vacancies = []
        for i in range(3):
            vacancy = Mock(spec=Vacancy)
            vacancy.salary = 100000 + i * 10000
            vacancies.append(vacancy)

        # Запрашиваем 5 вакансий, но есть только 3
        result = get_top_vacancies(vacancies, 5)

        # Должен вернуть все 3 вакансии
        assert len(result) == 3
        assert result[0].salary == 120000  # Самая высокая
        assert result[1].salary == 110000
        assert result[2].salary == 100000  # Самая низкая


if __name__ == "__main__":
    pytest.main(["-v", __file__])
