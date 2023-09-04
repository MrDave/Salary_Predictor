from handlers import get_sj_response, predict_sj_rub_salary
from math import ceil
from handlers import LANGUAGES


def get_sj_stats(sj_key, single_page=False):

    vacancies = {}

    for language in LANGUAGES:
        keyword = language
        vacancy_pages = []

        page_0 = get_sj_response(sj_key, keyword).json()
        number_found = page_0["total"]
        pages = ceil(number_found / 20)
        vacancy_pages.append(page_0)

        if not single_page:
            for page in range(1, pages):
                language_vacancy_page = get_sj_response(sj_key, keyword, page).json()
                vacancy_pages.append(language_vacancy_page)

        language_vacancies = []
        for page in vacancy_pages:
            language_vacancies.extend(vacancy for vacancy in page["objects"])

        predicted_salaries = []
        for vacancy in language_vacancies:
            predicted_salary = predict_sj_rub_salary(vacancy)
            if predicted_salary:
                predicted_salaries.append(predicted_salary)
        try:
            avg_salary = int(sum(predicted_salaries) / len(predicted_salaries))
        except ZeroDivisionError:
            avg_salary = "-"
        vacancies[language] = {
            "vacancies_found": number_found,
            "vacancies_processed": len(predicted_salaries),
            "average_salary": avg_salary
        }

    return vacancies
