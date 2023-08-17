from environs import Env
from pprint import pprint
import requests
from main import predict_salary
from argparse import ArgumentParser
import datetime
from time import sleep

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


def get_sj_vacancies(secret_key: str, keyword: str, page=0):

    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": secret_key
    }

    params = {
        "catalogues": 48,
        "town": 4,
        "keyword": keyword,
        "count": 20,
        "page": page
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response


def predict_sj_rub_salary(vacancy):
    if vacancy["currency"] != "rub":
        return None
    return predict_salary(vacancy["payment_from"], vacancy["payment_to"])


def main():
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
            sleep(0.5)

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
    sleep(2)

    pprint(vacancies, sort_dicts=False)
    end_time = datetime.datetime.now()
    run_time = (end_time - start_time).seconds
    if args.timer:
        print(f"Start time: {start_time}\nEnd time: {end_time}\nTotal time: {run_time} second(s)")


if __name__ == '__main__':
    main()
