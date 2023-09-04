from handlers import get_hh_response, predict_hh_rub_salary
from time import sleep
from handlers import LANGUAGES


def get_hh_stats(single_page=False):
    vacancies = {}

    for language in LANGUAGES:
        search_query = f"Программист {language}"

        vacancy_pages = []

        language_vacancy_page_0 = get_hh_response(search_query, period=30).json()
        number_found = language_vacancy_page_0["found"]
        pages = language_vacancy_page_0["pages"]
        vacancy_pages.append(language_vacancy_page_0)

        if not single_page:
            for page in range(1, pages):
                language_vacancies_page = get_hh_response(search_query, period=30, page=page).json()
                vacancy_pages.append(language_vacancies_page)
                sleep(0.5)

        language_vacancies = []
        for page in vacancy_pages:
            language_vacancies.extend(vacancy for vacancy in page["items"])

        predicted_salaries = []

        for vacancy in language_vacancies:
            predicted_salary = predict_hh_rub_salary(vacancy)
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
        sleep(2)

    return vacancies
