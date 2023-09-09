from terminaltables import AsciiTable


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


def print_job_table(vacancies, title):

    header_row = [
        "Language",
        "Vacancies Found",
        "Vacancies Processed",
        "Average Salary, RUB"
    ]
    table_content = [header_row]
    for language in vacancies.keys():
        new_row = [language] + list(vacancies[language].values())
        table_content.append(new_row)
    table = AsciiTable(table_content, title)
    print()
    print(table.table)
