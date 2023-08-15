import requests
from pprint import pprint
from argparse import ArgumentParser

# parser = ArgumentParser()
# parser.add_argument("-p", "--period")
# # parser.add_argument("-t","--text", help="vacancy search query")
#
# args = parser.parse_args()


def get_vacancies(search_query, period=None):

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

    # for language in languages_list:
    #     search_query = f"Программист {language}"
    #     vacancies[language] = get_vacancies(search_query).json()["found"]

    vacancies = get_vacancies("Программист Python", 30)

    for vacancy in vacancies.json()["items"]:
        predicted_salary = predict_rub_salary(vacancy)
        print(predicted_salary)
