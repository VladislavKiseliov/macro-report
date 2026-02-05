import csv
import sys
from typing import List, Dict
from pathlib import Path
import argparse
import csv
from tabulate import tabulate
from collections import defaultdict





class FileValidationError(Exception):
    """Base exception for file validation errors."""
    pass

def validate_files(file_paths: List[str]) -> List[Path]:
    """
    Validates a list of file paths.

    :param file_paths: List of raw string paths from arguments.
    :return: List of validated Path objects.
    :raises FileValidationError: If file doesn't exist, is a directory, or not CSV.
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
    """
        Reads multiple CSV files into a single list of dictionaries.

        :param file_paths: List of Path objects to read.
        :return: List of rows as dictionaries.
        """

    all_data = []
    for path in file_path:
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_data.append(row)
    return all_data


def generate_average_gdp(data:List[Dict])->List[Dict]:
    """
        Calculates the average GDP per country.

        :param data: Raw list of dictionaries from CSV.
        :return: Sorted list of dictionaries with average GDP.
    """
    state_groups = defaultdict(list)

    # Группируем данные, игнорируя некорректные строки
    for row in data:
        try:
            gdp_val = float(row["gdp"])
            state_groups[row["country"]].append(gdp_val)
        except (ValueError, KeyError, TypeError):
            # Пропускаем битые строки
            continue

    result = []
    for country in state_groups:
        avg_gdp = round(sum(state_groups[country]) / len(state_groups[country]),2)
        result.append({"country": country, "avg_gdp": avg_gdp})

    # Сортировка по убыванию ВВП
    result.sort(key=lambda x: x["avg_gdp"], reverse=True)
    return result

def print_report(report_data: List[Dict]):
    """
        Prints the report data in a formatted table.
    """

    table = [[row['country'], f"{row['avg_gdp']:.2f}"] for row in report_data]
    print(tabulate(table, headers=['Country', 'Avg GDP'], tablefmt='grid'))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+', required=True)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()

    # Реестр доступных отчетов
    REPORT_REGISTRY = {
        'average-gdp': generate_average_gdp,
        # 'new_report' : funk_new_report -- Для добавление нового типа отчетов
    }

    try:
        # Валидация путей
        file_paths = validate_files(args.files)

        # Загрузка данных
        data = read_csv(file_paths)
        if not data:
            print("Error: No data_examples found in files", file=sys.stderr)
            sys.exit(1)

        # Генерация отчёта
        report_func = REPORT_REGISTRY.get(args.report)
        if report_func:
            report_data = report_func(data)
        else:
            print(f"Unknown report: {args.report}")

        if not report_data:
            print("No data_examples to display")
            return

        # Вывод результата в консоль
        print_report(report_data)

    except FileValidationError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()