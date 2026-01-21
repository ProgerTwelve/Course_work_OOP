from src.class_vacancies import Vacancy

class TestVacancy:
    """Тесты для класса Vacancy."""

    def test_init_and_attributes(self):
        """Тест инициализации и атрибутов класса."""

        # Подготовка тестовых данных

        test_data = {
            "name": "Python Developer",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/123",
            "employer": {"name": "TechCompany", "id": "123"},
            "snippet": {"requirement": "Python, Django, REST API"},
            "experience": {"name": "От 1 года до 3 лет"},
            "employment": {"name": "Полная занятость"}
        }

        # Создание экземпляра

        vacancy = Vacancy(**test_data)

        # Проверка атрибутов

        assert vacancy.name == "Python Developer"
        assert vacancy.salary == 125000  # (100000 + 150000) / 2
        assert vacancy.alternate_url == "https://hh.ru/vacancy/123"
        assert vacancy.employer == "TechCompany"
        assert vacancy.snippet == "Python, Django, REST API"
        assert vacancy.experience == "От 1 года до 3 лет"
        assert vacancy.employment == "Полная занятость"

    def test_salary_validate_different_cases(self):
        """Тест валидации зарплаты в разных случаях."""

        # Случай 1: есть и from, и to

        salary1 = {"from": 100000, "to": 150000}
        result1 = Vacancy._Vacancy__salary_validate(salary1)
        assert result1 == 125000

        # Случай 2: только from

        salary2 = {"from": 100000, "to": None}
        result2 = Vacancy._Vacancy__salary_validate(salary2)
        assert result2 == 100000

        # Случай 3: только to

        salary3 = {"from": None, "to": 150000}
        result3 = Vacancy._Vacancy__salary_validate(salary3)
        assert result3 == 150000

        # Случай 4: нет ни from, ни to

        salary4 = {"from": None, "to": None}
        result4 = Vacancy._Vacancy__salary_validate(salary4)
        assert result4 == 0

    def test_str_method(self):
        """Тест строкового представления."""

        test_data = {
            "name": "Backend Developer",
            "salary": {"from": 120000, "to": None},
            "alternate_url": "https://hh.ru/vacancy/456",
            "employer": {"name": "IT Corp"},
            "snippet": {"requirement": "Python, FastAPI, PostgreSQL"},
            "experience": {"name": "Нет опыта"},
            "employment": {"name": "Удаленная работа"}
        }

        vacancy = Vacancy(**test_data)
        result = str(vacancy)

        # Проверяем наличие ключевых строк в выводе

        assert "Backend Developer" in result
        assert "120000 рублей" in result
        assert "https://hh.ru/vacancy/456" in result
        assert "IT Corp" in result
        assert "Python, FastAPI, PostgreSQL" in result
        assert "Нет опыта" in result
        assert "Удаленная работа" in result

    def test_comparison_methods(self):
        """Тест методов сравнения по зарплате."""

        # Создаем две вакансии с разными зарплатами
        vacancy1_data = {
            "name": "Junior",
            "salary": {"from": 50000, "to": 70000},
            "alternate_url": "url1",
            "employer": {"name": "Company A"},
            "snippet": {"requirement": "Python"},
            "experience": {"name": "Нет опыта"},
            "employment": {"name": "Полная занятость"}
        }

        vacancy2_data = {
            "name": "Senior",
            "salary": {"from": 150000, "to": 200000},
            "alternate_url": "url2",
            "employer": {"name": "Company B"},
            "snippet": {"requirement": "Python, Architecture"},
            "experience": {"name": "Более 6 лет"},
            "employment": {"name": "Полная занятость"}
        }

        vacancy1 = Vacancy(**vacancy1_data)  # salary = 60000
        vacancy2 = Vacancy(**vacancy2_data)  # salary = 175000

        # Проверка операторов сравнения

        assert vacancy1 < vacancy2  # __lt__
        assert vacancy2 > vacancy1  # __gt__
        assert not vacancy1 > vacancy2
        assert not vacancy2 < vacancy1

    def test_to_dict_method(self):
        """Тест преобразования в словарь."""

        test_data = {
            "name": "Data Scientist",
            "salary": {"from": 150000, "to": 200000},
            "alternate_url": "https://hh.ru/vacancy/789",
            "employer": {"name": "DataCompany"},
            "snippet": {"requirement": "Python, ML, SQL"},
            "experience": {"name": "От 3 до 6 лет"},
            "employment": {"name": "Гибкий график"}
        }

        vacancy = Vacancy(**test_data)
        result_dict = vacancy.to_dict()

        # Проверяем структуру и значения словаря

        assert isinstance(result_dict, dict)
        assert result_dict["name"] == "Data Scientist"
        assert result_dict["salary"] == 175000
        assert result_dict["alternate_url"] == "https://hh.ru/vacancy/789"
        assert result_dict["employer"] == "DataCompany"
        assert result_dict["snippet"] == "Python, ML, SQL"
        assert result_dict["experience"] == "От 3 до 6 лет"
        assert result_dict["employment"] == "Гибкий график"

    def test_edge_cases(self):
        """Тест граничных случаев и обработки ошибок."""

        # Случай с нулевой зарплатой
        test_data = {
            "name": "Intern",
            "salary": {"from": None, "to": None},
            "alternate_url": "https://hh.ru/vacancy/999",
            "employer": {"name": "Startup"},
            "snippet": {"requirement": ""},
            "experience": {"name": "Нет опыта"},
            "employment": {"name": "Стажировка"}
        }

        vacancy = Vacancy(**test_data)
        assert vacancy.salary == 0
        assert "0 рублей" in str(vacancy)
