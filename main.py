import requests
from pprint import pprint
from argparse import ArgumentParser
from time import sleep


parser = ArgumentParser()
parser.add_argument("-d", "--days")
parser.add_argument(
    "-p",
    "--pages",
    help="number of pages",
    type=int,
    choices=range(1, 100),
    metavar="[1-99]"
)

args = parser.parse_args()


def get_vacancies(search_query, period=None, page=0):

    url = "https://api.hh.ru/vacancies"

    headers = {
        "HH-User-Agent": ""
    }
    params = {
        "text": search_query,
        "area": 1,
        "period": period,
        "order_by": "relevance",
        "page": page
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response


def predict_rub_salary(vacancy):
    salary_info = vacancy["salary"]
    if salary_info is None or salary_info.get("currency") != "RUR":
        return None

    if salary_info.get("from") and salary_info.get("to"):
        predicted_salary = (salary_info.get("from") + salary_info.get("to")) / 2
    elif salary_info.get("from"):
        predicted_salary = salary_info.get("from") * 1.2
    elif salary_info.get("to"):
        predicted_salary = salary_info.get("to") * 0.8
    else:
        return None
    return predicted_salary


if __name__ == '__main__':

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
        pages = args.pages
        list_of_vacancies_pages = []

        for page in range(pages):
            language_vacancies_page = get_vacancies(search_query, period=args.days, page=page).json()
            list_of_vacancies_pages.append(language_vacancies_page)
            sleep(1)

        number_found = list_of_vacancies_pages[0]["found"]
        language_vacancies = []
        for vacancy_page in list_of_vacancies_pages:
            for vacancy in vacancy_page["items"]:
                language_vacancies.append(vacancy)

        predicted_salaries = []

        for vacancy in language_vacancies:
            predicted_salary = predict_rub_salary(vacancy)
            if predicted_salary is not None:
                predicted_salaries.append(predicted_salary)

        vacancies[language] = {
            "vacancies_found": number_found,
            "vacancies_processed": len(predicted_salaries),
            "average_salary": int(sum(predicted_salaries)/len(predicted_salaries))
        }
    sleep(5)

    pprint(vacancies, sort_dicts=False)
