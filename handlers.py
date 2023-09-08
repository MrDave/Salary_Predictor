import requests
from terminaltables import AsciiTable


LANGUAGES = [
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


def get_hh_response(search_query, period=None, page=0):

    url = "https://api.hh.ru/vacancies"

    headers = {
        "HH-User-Agent": ""
    }
    moscow_area_code = 1
    params = {
        "text": search_query,
        "area": moscow_area_code,
        "period": period,
        "order_by": "relevance",
        "page": page
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        predicted_salary = (salary_from + salary_to) / 2
    elif salary_from:
        predicted_salary = salary_from * 1.2
    elif salary_to:
        predicted_salary = salary_to * 0.8
    else:
        return None
    return predicted_salary


def predict_hh_rub_salary(vacancy):
    salary = vacancy["salary"]
    if not salary or salary.get("currency") != "RUR":
        return None
    predicted_hh_salary = predict_salary(salary.get("from"), salary.get("to"))
    return predicted_hh_salary


def get_sj_response(secret_key: str, keyword: str, page=0):

    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": secret_key
    }
    moscow_area_code = 4
    programming_jobs_catalogue = 48
    jobs_on_page = 20

    params = {
        "catalogues": programming_jobs_catalogue,
        "town": moscow_area_code,
        "keyword": keyword,
        "count": jobs_on_page,
        "page": page
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response


def predict_sj_rub_salary(vacancy):
    if vacancy["currency"] != "rub":
        return None
    return predict_salary(vacancy["payment_from"], vacancy["payment_to"])


def print_job_table(vacancies, title):

    header_row = [
        "Language",
        "Vacancies Found",
        "Vacancies Processed",
        "Average Salary, RUB"
    ]
    table_content = [header_row]
    for language in LANGUAGES:
        new_row = [language] + list(vacancies[language].values())
        table_content.append(new_row)
    table = AsciiTable(table_content, title)
    print()
    print(table.table)
