import requests
from pprint import pprint


def get_vacancies():

    url = "https://api.hh.ru/vacancies"
    headers = {
        "HH-User-Agent": ""
    }
    params = {
        "text": "Программист",
        "area": 1
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response

