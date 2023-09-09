import requests


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
