from typing import Any


class Vacancy:
    """Класс для работы с вакансиями."""

    __slots__ = (
        "name",
        "salary",
        "alternate_url",
        "employer",
        "snippet",
        "experience",
        "employment"
    )

    def __init__(
            self,
            name: str,
            salary: dict[int],
            alternate_url: str,
            employer: dict[str],
            snippet: dict[str],
            experience: dict[str],
            employment: dict[str]
    ) -> None:
        """Конструктор класса Vacancy."""

        self.name = name
        self.salary = self.__salary_validate(salary)
        self.alternate_url = alternate_url
        self.employer = employer["name"]
        self.snippet = snippet["requirement"]
        self.experience = experience["name"]
        self.employment = employment["name"]

    @staticmethod
    def __salary_validate(salary: dict[str | int]) -> int:
        """Приватный метод для определения среднего значения зарплаты, исходя из
        переданных данных в переменной salary."""

        # Проверка наличия from и to в salary и усредняем salary
        if isinstance(salary["from"], int) and isinstance(salary["to"], int):
            return int((int(salary["from"]) + int(salary["to"])) / 2)
        # Если есть только salary["from"]
        elif isinstance(salary["from"], int) and isinstance(salary["to"], type(None)):
            return int(salary["from"])
        # Если есть только salary["to"]
        elif isinstance(salary["from"], type(None)) and isinstance(salary["to"], int):
            return int(salary["to"])
        else:
            return 0

    def __str__(self) -> str:
        """Магический метод для представления информации об экземпляре объекта в виде строки. """

        return (f"Название вакансии   ----- {self.name}\n"
                f"Заработная плата    ----- {self.salary} рублей\n"
                f"Ссылка на вакансию  ----- {self.alternate_url}\n"
                f"Работодатель        ----- {self.employer}\n"
                f"Требования и навыки ----- {self.snippet}\n"
                f"Наличие опыта       ----- {self.experience}\n"
                f"Тип занятости       ----- {self.employment}\n"
                f"--------------------------------------------\n"
                )

    def __lt__(self, other: "Vacancy") -> bool:
        """Магический метод сравнения (self < other) вакансий по зарплате."""

        return self.salary < other.salary

    def __gt__(self, other: "Vacancy") -> bool:
        """Магический метод сравнения (self > other) вакансий по зарплате."""

        return self.salary > other.salary

    def to_dict(self) -> dict[str, str | int | Any]:
        """Метод для преобразования экземпляра класса в словарь."""

        return {
            "name": self.name,
            "salary": self.salary,
            "alternate_url": self.alternate_url,
            "employer": self.employer,
            "snippet": self.snippet,
            "experience": self.experience,
            "employment": self.employment
        }
