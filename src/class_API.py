import requests
from src.class_Parser import Parser

class HH(Parser):
    """Класс для работы с API HeadHunter."""

    def __init__(self) -> None:
        """Конструктор класса HH, который закладывает логику подключения к API HH.ru,
        и подготавливает список для последующего добавления в него вакансий."""

        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100, 'only_with_salary': True}
        self.vacancies = []

    def _get_connection(self) -> bool | None:
        """Метод подключения к API сайта HH.ru"""

        try:
            response = requests.get(url=self.__url, headers=self.__headers)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            print("Ошибка соединения с сайтом")

    def load_vacancies(self, keyword: str) -> None:
        """Метод для загрузки списка словарей вакансий с сайта hh.ru
        keyword - ключевое слово или слова, по которым будет произведен поиск
        и добавление вакансий."""

        if self._get_connection():
            self.__params['text'] = keyword
            while self.__params.get('page') != 20:
                response = requests.get(url=self.__url, headers=self.__headers, params=self.__params)
                vacancies = response.json()['items']
                self.vacancies.extend(vacancies)
                self.__params['page'] += 1
        else:
            print("Ошибка загрузки данных с вакансиями.")

if __name__ == "__main__":
    import json

    p = HH()
    p.load_vacancies("Python-разработчик")
    for vacancy in p.vacancies[0:10]:
        print(json.dumps(vacancy, indent=4, ensure_ascii=False))
        print(f"-----------------------------------------------")

