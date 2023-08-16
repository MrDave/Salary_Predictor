from environs import Env
import requests


def get_sj_vacancies(secret_key: str):

    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": secret_key
    }

    params = {

    }


def main():
    env = Env
    env.read_env()

    sj_key = env.str("SJ_KEY")


