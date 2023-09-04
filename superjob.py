from argparse import ArgumentParser
from environs import Env
from handlers import get_sj_response, predict_sj_rub_salary, print_job_table
from math import ceil
import datetime
from main import LANGUAGES


def get_sj_stats(sj_key, args):

    vacancies = {}

    for language in LANGUAGES:
        keyword = language
        vacancy_pages = []

        language_vacancy_page_0 = get_sj_response(sj_key, keyword).json()
        number_found = language_vacancy_page_0["total"]
        pages = ceil(number_found / 20)
        vacancy_pages.append(language_vacancy_page_0)

        if not args.single:
            for page in range(1, pages):
                language_vacancy_page = get_sj_response(sj_key, keyword, page).json()
                vacancy_pages.append(language_vacancy_page)

        language_vacancies = []
        for page in vacancy_pages:
            language_vacancies.extend(vacancy for vacancy in page["objects"])

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

    return vacancies


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

    start_time = datetime.datetime.now()

    sj_jobs = get_sj_stats(sj_key, args)
    table_title = "SuperJob Moscow"
    print_job_table(sj_jobs, table_title)

    end_time = datetime.datetime.now()
    run_time = (end_time - start_time).seconds
    if args.timer:
        print(f"Start time: {start_time}\nEnd time: {end_time}\nTotal time: {run_time} second(s)")
