import csv
import sys
from typing import List, Dict
from pathlib import Path
import argparse
import csv
from collections import defaultdict
from tabulate import tabulate

class FileValidationError(Exception):
    """Базовое исключение для ошибок валидации файлов"""
    pass

def validate_files(file_paths: List[str]) -> List[Path]:
    """
    Проверяет список путей и возвращает валидные Path-объекты.
    Выбрасывает исключения если файл ненайден или не соответсвует формату
    """
    valid_paths = []

    for raw_path in file_paths:
        path = Path(raw_path)

        # Проверяем существует ли файл:
        if not path.exists():
            raise FileValidationError(f"File not found: {raw_path}")

        # Проверяем файл это или директория
        if not path.is_file():
            raise FileValidationError(f"Not a file: {raw_path}")

        # Проверяем расширение файла .
        if path.suffix.lower() != '.csv':
            raise FileValidationError(
                f"Expected .csv file, got '{path.suffix}': {raw_path}"
            )

        valid_paths.append(path)

    return valid_paths



def read_csv(file_path:List[Path])->List[Dict]:
    """Читаем все файлы в один список словарей"""
    all_data = []
    for path in file_path:
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                print(f"{row=}")
                all_data.extend(row)
    return all_data



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+', required=True)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()

    try:
        # Валидация путей
        file_paths = validate_files(args.files)

        # Загрузка данных
        data = read_csv(file_paths)
        if not data:
            print("Error: No data_examples found in files", file=sys.stderr)
            sys.exit(1)

        # Генерация отчёта
        if args.report == 'average-gdp':
            report_data = generate_average_gdp_report(data)
        else:
            raise ValueError(f"Unknown report: {args.report}")

        if not report_data:
            print("No data_examples to display")
            return

        # Вывод результата в консоль
        # print_report(report_data)

    except FileValidationError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)



if __name__ == '__main__':
    file_path1 = Path('data_examples/economic1.csv')
    file_path2 = Path('data_examples/economic2.csv')
    resulr = read_csv([file_path1, file_path2])