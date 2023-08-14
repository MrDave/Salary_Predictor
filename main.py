import requests
from pprint import pprint
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-p", "--period", default=30)

args = parser.parse_args()


def get_vacancies(period):

    url = "https://api.hh.ru/vacancies"

    headers = {
        "HH-User-Agent": ""
    }
    params = {
        "text": "Программист",
        "area": 1,
        "period": period,
        "order_by": "relevance"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response


if __name__ == '__main__':
    vacancies = get_vacancies(args.period)

    pprint(vacancies.text)
    print(vacancies.url)
