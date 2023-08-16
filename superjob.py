from environs import Env
from pprint import pprint
import requests


def get_sj_vacancies(secret_key: str):

    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": secret_key
    }

    params = {
        "catalogues": 48,
        "town": 4
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response


def main():
    env = Env()
    env.read_env()

    sj_key = env.str("SJ_KEY")
    vacancies = get_sj_vacancies(sj_key)

    for vacancy in vacancies.json()["objects"]:
        print(vacancy["profession"], vacancy["town"]["title"], sep=", ")


if __name__ == '__main__':
    main()

