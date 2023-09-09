from handlers import get_hh_response, predict_hh_rub_salary
from time import sleep


def get_hh_stats(lang_list, single_page=False):
    vacancy_stats = {}

    for language in lang_list:
        search_query = f"Программист {language}"

        vacancies = []

        page_0 = get_hh_response(search_query, period=30).json()
        number_found = page_0["found"]
        pages = page_0["pages"]
        vacancies.extend(page_0["items"])

        if not single_page:
            for page in range(1, pages):
                vacancy_page = get_hh_response(search_query, period=30, page=page).json()
                vacancies.extend(vacancy_page["items"])
                sleep(0.5)

        predicted_salaries = []

        for vacancy in vacancies:
            predicted_salary = predict_hh_rub_salary(vacancy)
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
        sleep(2)

    return vacancy_stats
