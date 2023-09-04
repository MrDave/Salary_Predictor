from argparse import ArgumentParser
from handlers import get_hh_response, predict_hh_rub_salary, print_job_table
from time import sleep
import datetime

from main import LANGUAGES


def get_hh_stats(args):
    vacancies = {}

    for language in LANGUAGES:
        search_query = f"Программист {language}"

        vacancy_pages = []

        language_vacancy_page_0 = get_hh_response(search_query, period=30).json()
        number_found = language_vacancy_page_0["found"]
        pages = language_vacancy_page_0["pages"]
        vacancy_pages.append(language_vacancy_page_0)

        if not args.single:
            for page in range(1, pages):
                language_vacancies_page = get_hh_response(search_query, period=30, page=page).json()
                vacancy_pages.append(language_vacancies_page)
                sleep(0.5)

        language_vacancies = []
        for page in vacancy_pages:
            language_vacancies.extend(vacancy for vacancy in page["items"])

        predicted_salaries = []

        for vacancy in language_vacancies:
            predicted_salary = predict_hh_rub_salary(vacancy)
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
        sleep(2)

    return vacancies


if __name__ == '__main__':
    parser = ArgumentParser(
        description="Get job offers from HeadHunter website and compare their average salaries"
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

    hh_stats = get_hh_stats(args)
    table_title = "HeadHunter Moscow"
    print_job_table(hh_stats, table_title)

    end_time = datetime.datetime.now()
    run_time = (end_time - start_time).seconds
    if args.timer:
        print(f"Start time: {start_time}\nEnd time: {end_time}\nTotal time: {run_time} second(s)")