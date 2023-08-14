import requests
from pprint import pprint
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-p", "--period")

args = parser.parse_args()


def get_vacancies(search_query, period=30):

    url = "https://api.hh.ru/vacancies"

    headers = {
        "HH-User-Agent": ""
    }
    params = {
        "text": search_query,
        "area": 1,
        "period": period,
        "order_by": "relevance"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response


def get_salary(vacancy):
    return vacancy["salary"]


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
        vacancies[language] = get_vacancies(search_query).json()["found"]

    python_vacancies = get_vacancies("Программист Python")
    for vacancy in python_vacancies.json()["items"]:
        print(get_salary(vacancy))
