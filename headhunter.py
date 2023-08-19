from argparse import ArgumentParser
from functions import get_hh_page_count, get_hh_vacancies, predict_hh_rub_salary
from terminaltables import AsciiTable
from time import sleep
import datetime


def print_hh_table():
    parser = ArgumentParser()
    parser.add_argument(
        "-d",
        "--days",
        default=30
    )
    parser.add_argument(
        "-p",
        "--pages",
        help="number of pages",
        type=int,
        choices=range(1, 100),
        metavar="[1-99]",
        default=1
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

    start_time = datetime.datetime.now()

    vacancies = {}
    languages_list = [
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

    for language in languages_list:
        search_query = f"Программист {language}"

        list_of_vacancies_pages = []

        language_vacancies_page_0 = get_hh_vacancies(search_query, 30).json()
        number_found = language_vacancies_page_0["found"]
        pages = get_hh_page_count(language_vacancies_page_0)
        list_of_vacancies_pages.append(language_vacancies_page_0)

        # if not args.single:
        #     for page in range(1, pages):
        #         language_vacancies_page = get_hh_vacancies(search_query, period=args.days, page=page).json()
        #         list_of_vacancies_pages.append(language_vacancies_page)
        #         sleep(0.5)

        language_vacancies = []
        for vacancy_page in list_of_vacancies_pages:
            for vacancy in vacancy_page["items"]:
                language_vacancies.append(vacancy)

        predicted_salaries = []

        for vacancy in language_vacancies:
            predicted_salary = predict_hh_rub_salary(vacancy)
            if predicted_salary is not None:
                predicted_salaries.append(predicted_salary)

        vacancies[language] = {
            "vacancies_found": number_found,
            "vacancies_processed": len(predicted_salaries),
            "average_salary": int(sum(predicted_salaries)/len(predicted_salaries))
        }
    sleep(2)

    header_row = [
        "Language",
        "Vacancies Found",
        "Vacancies Processed",
        "Average Salary, RUB"
    ]
    table_data = [header_row]
    for language in languages_list:
        new_row = [language] + list(vacancies[language].values())
        table_data.append(new_row)
    table = AsciiTable(table_data, "HeadHunter Moscow")
    print()
    print(table.table)

    end_time = datetime.datetime.now()
    run_time = (end_time - start_time).seconds
    if args.timer:
        print(f"Start time: {start_time}\nEnd time: {end_time}\nTotal time: {run_time} second(s)")


if __name__ == '__main__':
    print_hh_table()
