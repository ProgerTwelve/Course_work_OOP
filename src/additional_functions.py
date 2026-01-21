from src.class_API import HH
from src.class_vacancies import Vacancy


def check_currency(data: HH) -> list:
    """Функция для отсеивания вакансий из класса HH, которая группирует только
    вакансии с зарплатой в рублях для последующего преобразования этих вакансий
    в объекты класса Vacancy."""

    vacancy_rur = []
    for d in data.vacancies:
        if d["salary"]["currency"] == "RUR":
            vacancy_rur.append(d)

    return vacancy_rur


def vacancy_objects(vacancy_hh: list) -> list[Vacancy]:
    """Функция создания списка с объектами класса Vacancy из списка вакансий, полученного
    от API HH.ru."""

    vacancyies_object = []
    for vac in vacancy_hh:
        v = Vacancy(
            vac["name"],
            vac["salary"],
            vac["alternate_url"],
            vac["employer"],
            vac["snippet"],
            vac["experience"],
            vac["employment"]
        )
        vacancyies_object.append(v)

    return vacancyies_object


def filter_vacancies(vacancies: list[Vacancy], keywords: list[str]) -> list[Vacancy]:
    """"Функция поиска вакансий по ключевым словам."""

    filtered_vacancies = []

    for vac in vacancies:
        if any(word.lower() in vac.name.lower() for word in keywords):
            filtered_vacancies.append(vac)

    return filtered_vacancies


def get_vacancies_by_salary(vacancies: list[Vacancy], salary_range: list[str]) -> list[Vacancy]:
    """Функция для фильтрования списка вакансий по диапазону зарплат."""

    vacancies_by_salary = []
    salary_from = int(salary_range[0])
    salary_to = int(salary_range[1])

    for vac in vacancies:
        if salary_from <= vac.salary <= salary_to:
            vacancies_by_salary.append(vac)

    return vacancies_by_salary


def sort_vacancies(vacancies: list[Vacancy]) -> list[Vacancy]:
    """Функция для сортировки списка объектов вакансий по убываеию зарплаты."""

    sorted_vacancies = sorted(vacancies, key=lambda vac: vac.salary, reverse=True)

    return sorted_vacancies


def get_top_vacancies(vacancies: list[Vacancy], top_n: int) -> list[Vacancy]:
    """Функция, которая возвращает список из топ N вакансий."""

    sorted_vacancies = sort_vacancies(vacancies)

    return sorted_vacancies[:top_n]
