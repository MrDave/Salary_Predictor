from environs import Env
from pprint import pprint
from functions import get_sj_vacancies, predict_sj_rub_salary
from argparse import ArgumentParser
import datetime


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-p",
        "--pages",
        help="number of pages",
        type=int,
        choices=range(1, 25),
        metavar="[1-25]",
        default=1
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
        keyword = language
        pages = args.pages
        list_of_vacancies_pages = []

        for page in range(pages):
            language_vacancies_page = get_sj_vacancies(sj_key, keyword, page).json()
            list_of_vacancies_pages.append(language_vacancies_page)

        number_found = list_of_vacancies_pages[0]["total"]
        language_vacancies = []
        for vacancy_page in list_of_vacancies_pages:
            for vacancy in vacancy_page["objects"]:
                language_vacancies.append(vacancy)

        predicted_salaries = []
        for vacancy in language_vacancies:
            predicted_salary = predict_sj_rub_salary(vacancy)
            if predicted_salary is not None:
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

    pprint(vacancies, sort_dicts=False)
    end_time = datetime.datetime.now()
    run_time = (end_time - start_time).seconds
    if args.timer:
        print(f"Start time: {start_time}\nEnd time: {end_time}\nTotal time: {run_time} second(s)")


if __name__ == '__main__':
    main()
