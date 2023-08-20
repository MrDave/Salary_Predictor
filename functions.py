from math import ceil

import requests


def get_hh_page_count(response_dict):
    page_count = response_dict["pages"]
    if page_count > 99:
        return 99
    else:
        return page_count - 1


def get_sj_page_count(response_dict):
    page_count = ceil(response_dict["total"] / 20)
    if page_count > 25:
        return 24
    else:
        return page_count - 1


def get_hh_vacancies(search_query, period=None, page=0):

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
    salary_info = vacancy["salary"]
    if salary_info is None or salary_info.get("currency") != "RUR":
        return None
    predicted_hh_salary = predict_salary(salary_info.get("from"), salary_info.get("to"))
    return predicted_hh_salary


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