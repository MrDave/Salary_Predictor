from handlers import get_sj_response, predict_sj_rub_salary
from math import ceil


def get_sj_stats(sj_key, lang_list, single_page=False):

    vacancy_stats = {}

    for language in lang_list:
        keyword = language
        vacancies = []

        jobs_on_page = 20
        page_0 = get_sj_response(sj_key, keyword).json()
        number_found = page_0["total"]
        pages = ceil(number_found / jobs_on_page)
        vacancies.extend(page_0["objects"])

        if not single_page:
            for page in range(1, pages):
                vacancy_page = get_sj_response(sj_key, keyword, page).json()
                vacancies.extend(vacancy_page["objects"])

        predicted_salaries = []
        for vacancy in vacancies:
            predicted_salary = predict_sj_rub_salary(vacancy)
            if predicted_salary:
                predicted_salaries.append(predicted_salary)
        try:
            avg_salary = int(sum(predicted_salaries) / len(predicted_salaries))
        except ZeroDivisionError:
            avg_salary = "-"
        vacancy_stats[language] = {
            "vacancies_found": number_found,
            "vacancies_processed": len(predicted_salaries),
            "average_salary": avg_salary
        }

    return vacancy_stats
