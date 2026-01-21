import json
from typing import Any

from src.class_API import HH
from src.class_abs_file_work import FileWorker
from src.class_vacancies import Vacancy


class JSONFileWorker(FileWorker):
    """Класс для загрузки, получения и удаления данных о полученных вакансиях в файл в формате JSON.
    Является дочерним от класса FileWorker."""

    def __init__(self, filename: str ="../data/vacancy.json"):
        """Конструктор класса JSONFileWorker."""

        self.__filename = filename

    def get_data(self) -> Any | None:
        """Метод получения данных о вакансиях из JSON-файла."""

        # Если файл существует, читаем данные
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
            return existing_data
        except (FileNotFoundError, json.JSONDecodeError):
            print("Файл не существует или пустой/поврежден.")

    def load_data(self, vacancies: list[Vacancy]) -> None:
        """Метод добавления данных о вакансиях в JSON-файл."""

        # Сначала собираем все данные в список словарей
        all_vacancies = []

        # Если файл существует, читаем старые данные
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                if isinstance(existing_data, list):
                    all_vacancies = existing_data
        except (FileNotFoundError, json.JSONDecodeError):
            # Если файла нет или он пустой/поврежден, начинаем с пустого списка
            all_vacancies = []

        # Собираем URL уже существующих вакансий, чтобы избежать дублирования
        existing_urls = {v.get('alternate_url') for v in all_vacancies if v.get('alternate_url')}

        # Добавляем только новые уникальные вакансии
        for v in vacancies:
            if v.alternate_url not in existing_urls:
                all_vacancies.append(v.to_dict())
                existing_urls.add(v.alternate_url)  # Обновляем множество для контроля дубликатов

        # Записываем весь список обратно в файл
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(all_vacancies, f, ensure_ascii=False, indent=4)

    def delete_data(self, url: str) -> None:
        """Метод для удаления данных о вакансиях по ключу alternate_url из JSON-файла."""

        # Если файл существует, читаем старые данные
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                existing_data = json.load(f)

            # Удаляем данные по ключу alternate_url
            existing_data = [vacancy for vacancy in existing_data if vacancy["alternate_url"] != url]

            # Сохраняем данные обратно в файл
            with open(self.__filename, "w", encoding="utf-8") as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Файла нет или он пустой/поврежден")


if __name__ == "__main__":
    p = HH()
    p.load_vacancies("Python-разработчик")
    vacancy_list = []
    for r in p.vacancies:
        y = Vacancy(r["name"], r["salary"], r["alternate_url"], r["employer"], r["snippet"], r["experience"], r["employment"])
        vacancy_list.append(y)
    g = JSONFileWorker()
    g.delete_data("https://hh.ru/vacancy/128981553")
    print(g.get_data())
