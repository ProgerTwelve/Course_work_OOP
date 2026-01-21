from src.additional_functions import (check_currency, vacancy_objects, filter_vacancies,
                                      get_vacancies_by_salary, get_top_vacancies)
from src.class_API import HH
from src.class_file_work import JSONFileWorker


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем.
    Объединяет в себе все модули программы."""

    print("Здравствуйте! Это программа для поиска вакансий с сайта HH.ru")

    search = input("Какую вакансию вы хотите найти?:")

    vacancy_from_hh_ru = HH()
    vacancy_from_hh_ru.load_vacancies(search)

    print("Производится поиск вакансий с валютой в рублях....")

    vacancy_rub = check_currency(vacancy_from_hh_ru)

    print("Производится преобразование списка в список объектов класса Vacancy....")

    vacancies = vacancy_objects(vacancy_rub)
    print(f"По вашему запросу найдено {len(vacancies)} вакансий.")

    print("Производится сохранение вакансий в файл vacancy.json....")

    save_to_file = JSONFileWorker()
    save_to_file.load_data(vacancies)

    filter_words = input("Введите ключевые слова через пробел для фильтрации вакансий: ").split()

    filtered_vacancies = filter_vacancies(vacancies, filter_words)
    print(f"По вашему запросу найдено {len(filtered_vacancies)} вакансий. ")

    print("Производится сохранение вакансий в файл vacancy_filtered.json....")
    save_to_file_1 = JSONFileWorker("data/vacancy_filtered.json")
    save_to_file_1.load_data(filtered_vacancies)

    salary_range = input("Введите диапазон зарплат через дефис: ").split("-")
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    print(f"По диапазону {salary_range} рублей найдено {len(ranged_vacancies)} вакансий.")

    print("Производится сохранение вакансий в файл vacancy_filter_salary.json....")
    save_to_file_2 = JSONFileWorker("data/vacancy_filter_salary.json")
    save_to_file_2.load_data(ranged_vacancies)

    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    top_vacancies = get_top_vacancies(ranged_vacancies, top_n)

    for top in top_vacancies:
        print(top)
