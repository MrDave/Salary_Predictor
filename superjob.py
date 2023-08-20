from argparse import ArgumentParser
from environs import Env
from functions import get_sj_response, predict_sj_rub_salary
from math import ceil
from terminaltables import AsciiTable
import datetime


def print_sj_table(sj_key, args):
    start_time = datetime.datetime.now()

    vacancies = {}
    languages = [
        "JavaScript",
        "Java",
        "Python",
        "Ruby",
        "PHP",
        "C++",
        "C#",
        "C",
        "Go",
        "Shell"
    ]

    for language in languages:
        keyword = language
        vacancies_pages = []

        language_vacancies_page_0 = get_sj_response(sj_key, keyword).json()
        number_found = language_vacancies_page_0["total"]
        pages = ceil(number_found / 20)
        vacancies_pages.append(language_vacancies_page_0)

        if not args.single:
            for page in range(1, pages):
                language_vacancies_page = get_sj_response(sj_key, keyword, page).json()
                vacancies_pages.append(language_vacancies_page)

        language_vacancies = []
        for vacancy_page in vacancies_pages:
            for vacancy in vacancy_page["objects"]:
                language_vacancies.append(vacancy)

        predicted_salaries = []
        for vacancy in language_vacancies:
            predicted_salary = predict_sj_rub_salary(vacancy)
            if predicted_salary:
                predicted_salaries.append(predicted_salary)
        try:
            avg_salary = int(sum(predicted_salaries) / len(predicted_salaries))
        except ZeroDivisionError:
            avg_salary = "-"
        vacancies[language] = {
            "vacancies_found": number_found,
            "vacancies_processed": len(predicted_salaries),
            "average_salary": avg_salary
        }

    header_row = [
        "Language",
        "Vacancies Found",
        "Vacancies Processed",
        "Average Salary, RUB"
    ]
    table_data = [header_row]
    for language in languages:
        new_row = [language] + list(vacancies[language].values())
        table_data.append(new_row)
    table = AsciiTable(table_data, "SuperJob Moscow")
    print()
    print(table.table)

    end_time = datetime.datetime.now()
    run_time = (end_time - start_time).seconds
    if args.timer:
        print(f"Start time: {start_time}\nEnd time: {end_time}\nTotal time: {run_time} second(s)")


if __name__ == '__main__':
    parser = ArgumentParser(
        description="Get job offers from and SuperJob website and compare their average salaries"
    )
    parser.add_argument(
        "-s",
        "--single",
        help="fetch only a single page instead of all",
        action="store_true"
    )
    parser.add_argument(
        "-t",
        "--timer",
        action="store_true",
        help="add start and end time of script running after the results"
    )

    args = parser.parse_args()

    env = Env()
    env.read_env()

    sj_key = env.str("SJ_KEY")

    print_sj_table(sj_key, args)
