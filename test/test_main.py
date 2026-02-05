import pytest
from main import generate_average_gdp, validate_files, FileValidationError,read_csv

def test_generate_average_gdp_logic():
    # Готовим синтетические данные
    data = [
        {'country': 'A', 'gdp': '100'},
        {'country': 'A', 'gdp': '200'},
        {'country': 'B', 'gdp': '500'}
    ]
    result = generate_average_gdp(data)

    # Проверяем количество стран в отчете
    assert len(result) == 2
    # Проверяем сортировку (B должна быть первой, так как 500 > 150)
    assert result[0]['country'] == 'B'
    # Проверяем точность расчета (100 + 200) / 2 = 150.0
    assert result[1]['avg_gdp'] == 150.0


def test_generate_average_gdp_with_bad_data():
    data = [
        {'country': 'ValidCountry', 'gdp': '1000'},
        {'country': 'BrokenCountry', 'gdp': 'not_a_number'},  # Ошибка в числе
        {'country': 'MissingData', 'gdp': None}  # Данных нет
    ]
    result = generate_average_gdp(data)

    # Должна остаться только одна валидная страна
    assert len(result) == 1
    assert result[0]['country'] == 'ValidCountry'

def test_generate_average_gdp_empty():
    assert generate_average_gdp([]) == []


def test_validate_files_wrong_extension(tmp_path):
    """Проверка: файл существует, но он не .csv"""
    # Создаем временный текстовый файл
    fake_file = tmp_path / "data.txt"
    fake_file.write_text("some data")

    with pytest.raises(FileValidationError) as excinfo:
        validate_files([str(fake_file)])

    assert "Expected .csv file" in str(excinfo.value)


def test_read_csv_real_file(tmp_path):
    # 1. Создаем путь к временному файлу в папке tmp_path
    d = tmp_path / "sub"
    d.mkdir()
    test_file = d / "test.csv"

    # Записываем тестовые данные
    test_file.write_text("country,gdp\nRussia,100")
    # Читаем файл
    data = read_csv([test_file])

    # 4. Проверяем результат
    assert data[0]["country"] == "Russia"
    assert data[0]["gdp"] == "100"