import pytest
from unittest.mock import Mock
from src.class_API import HH


class TestHH:
    """Тесты для класса HH (HeadHunter API)"""

    def test_hh_initialization(self):
        """Тест инициализации класса HH"""
        hh = HH()

        assert hh._HH__url == 'https://api.hh.ru/vacancies'
        assert hh._HH__headers == {'User-Agent': 'HH-User-Agent'}
        assert hh._HH__params == {
            'text': '',
            'page': 0,
            'per_page': 100,
            'only_with_salary': True
        }
        assert hh.vacancies == []

    @pytest.mark.parametrize("status_code,expected", [
        (200, True),
        (404, None),
        (500, None),
    ])
    def test_get_connection_success(self, mocker, status_code, expected):
        """Тест метода _get_connection с разными статус-кодами"""

        hh = HH()
        mock_response = Mock()
        mock_response.status_code = status_code

        # Мокаем requests.get
        mock_get = mocker.patch('requests.get', return_value=mock_response)

        result = hh._get_connection()

        # Assert
        mock_get.assert_called_once_with(
            url=hh._HH__url,
            headers=hh._HH__headers
        )
        assert result == expected

    def test_load_vacancies_failed_connection(self, mocker, capsys):
        """Тест загрузки вакансий при неудачном подключении"""

        hh = HH()
        keyword = "Python разработчик"

        # Мокаем _get_connection чтобы вернуть None
        mocker.patch.object(hh, '_get_connection', return_value=None)

        # Мокаем requests.get чтобы убедиться что он не вызывается
        mock_get = mocker.patch('requests.get')

        hh.load_vacancies(keyword)

        # Capture output
        captured = capsys.readouterr()

        # Проверяем что _get_connection был вызван
        assert hh._get_connection.call_count == 1

        # Проверяем что requests.get не вызывался
        mock_get.assert_not_called()

        # Проверяем что список вакансий пуст
        assert hh.vacancies == []

        # Проверяем вывод сообщения об ошибке
        assert "Ошибка загрузки данных с вакансиями." in captured.out

    def test_load_vacancies_with_realistic_mock_data(self, mocker):
        """Тест с более реалистичными данными вакансий"""

        hh = HH()

        # Мокаем подключение
        mocker.patch.object(hh, '_get_connection', return_value=True)

        # Создаем разные данные для разных страниц
        def mock_response_generator():
            """Генератор mock ответов с разными данными для разных страниц"""
            for page in range(20):
                mock_resp = Mock()
                # Создаем уникальные вакансии для каждой страницы
                mock_vacancies = [
                    {
                        'id': f'{page}_{i}',
                        'name': f'Вакансия {page}_{i}',
                        'salary': {'from': 100000 + page * 1000, 'to': 150000 + page * 1000},
                        'employer': {'name': f'Компания {page}'},
                        'snippet': {'requirement': 'Требования'},
                        'alternate_url': f'https://hh.ru/vacancy/{page}_{i}'
                    }
                    for i in range(5)  # 5 вакансий на странице
                ]
                mock_resp.json.return_value = {'items': mock_vacancies}
                yield mock_resp

        # Создаем side_effect для имитации разных ответов на разных страницах
        mock_get = mocker.patch('requests.get')
        mock_get.side_effect = list(mock_response_generator())

        hh.load_vacancies("Python")

        # Проверяем что было 20 вызовов
        assert mock_get.call_count == 20

        # Проверяем что всего загружено 100 вакансий (20 страниц × 5 вакансий)
        assert len(hh.vacancies) == 100

        # Проверяем что страницы увеличивались
        assert hh._HH__params['page'] == 20

        # Проверяем что вакансии с разных страниц загружены
        assert hh.vacancies[0]['id'] == '0_0'  # Первая вакансия с первой страницы
        assert hh.vacancies[99]['id'] == '19_4'  # Последняя вакансия с последней страницы

    @pytest.mark.parametrize("keyword", [
        "Python разработчик",
        "Data Scientist",
        " ",
        "",
    ])
    def test_load_vacancies_with_different_keywords(self, mocker, keyword):
        """Тест загрузки вакансий с разными ключевыми словами"""

        hh = HH()

        # Мокаем подключение и requests
        mocker.patch.object(hh, '_get_connection', return_value=True)
        mock_response = Mock()
        mock_response.json.return_value = {'items': []}
        mocker.patch('requests.get', return_value=mock_response)

        hh.load_vacancies(keyword)

        # Проверяем что параметр text установлен правильно
        assert hh._HH__params['text'] == keyword

    def test_load_vacancies_stops_at_page_20(self, mocker):
        """Тест что загрузка останавливается на 20 странице"""

        hh = HH()

        # Мокаем подключение
        mocker.patch.object(hh, '_get_connection', return_value=True)

        # Создаем бесконечный генератор ответов
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'id': '1'}]}
        mock_get = mocker.patch('requests.get', return_value=mock_response)

        hh.load_vacancies("Test")

        # Проверяем что было ровно 20 вызовов
        assert mock_get.call_count == 20

        # Проверяем что параметр page стал равен 20
        assert hh._HH__params['page'] == 20

    def test_vacancies_structure(self, mocker):
        """Тест структуры возвращаемых вакансий"""

        hh = HH()

        # Мокаем подключение
        mocker.patch.object(hh, '_get_connection', return_value=True)

        # Создаем тестовые данные с полной структурой
        mock_vacancy = {
            'id': '123456',
            'name': 'Senior Python Developer',
            'area': {'name': 'Москва'},
            'salary': {
                'from': 200000,
                'to': 300000,
                'currency': 'RUR'
            },
            'employer': {
                'id': '12345',
                'name': 'Яндекс',
                'alternate_url': 'https://hh.ru/employer/12345'
            },
            'snippet': {
                'requirement': 'Опыт работы от 3 лет...',
                'responsibility': 'Разработка backend...'
            },
            'schedule': {'name': 'Полный день'},
            'experience': {'name': 'От 3 до 6 лет'},
            'employment': {'name': 'Полная занятость'},
            'alternate_url': 'https://hh.ru/vacancy/123456',
            'published_at': '2024-01-15T10:00:00+0300'
        }

        mock_response = Mock()
        mock_response.json.return_value = {'items': [mock_vacancy]}
        mocker.patch('requests.get', return_value=mock_response)

        hh.load_vacancies("Python")

        assert len(hh.vacancies) == 20  # 20 страниц по 1 вакансии

        # Проверяем структуру первой вакансии
        vacancy = hh.vacancies[0]
        assert 'id' in vacancy
        assert 'name' in vacancy
        assert 'salary' in vacancy
        assert 'employer' in vacancy
        assert 'alternate_url' in vacancy
        assert vacancy['salary']['from'] == 200000
        assert vacancy['employer']['name'] == 'Яндекс'

    def test_only_with_salary_parameter(self, mocker):
        """Тест что параметр only_with_salary всегда True"""

        hh = HH()

        # Мокаем подключение и requests
        mocker.patch.object(hh, '_get_connection', return_value=True)
        mock_response = Mock()
        mock_response.json.return_value = {'items': []}
        mock_get = mocker.patch('requests.get', return_value=mock_response)

        hh.load_vacancies("Test")

        # Проверяем что параметр only_with_salary установлен в True
        for call_args in mock_get.call_args_list:
            params = call_args[1]['params']
            assert params['only_with_salary'] is True
