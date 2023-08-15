import requests
from pprint import pprint


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
        language_vacancies = get_vacancies(search_query, 30).json()
        predicted_salaries = []

        for vacancy in language_vacancies["items"]:
            predicted_salary = predict_rub_salary(vacancy)
            if predicted_salary is not None:
                predicted_salaries.append(predicted_salary)

        vacancies[language] = {
            "vacancies_found": language_vacancies["found"],
            "vacancies_processed": len(predicted_salaries),
            "average_salary": int(sum(predicted_salaries)/len(predicted_salaries))
        }

    pprint(vacancies, sort_dicts=False)
