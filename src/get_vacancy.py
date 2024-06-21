import requests


def get_companies():
    """
    Получает информацию о компаниях, включая их имена и идентификаторы.

    :return: Список словарей с информацией о компаниях.
    :rtype: list[dict]
    """
    companies_data = {'Тиньков': 78638, 'Яндекс': 1740, 'Amex Development': 5724503, 'Сбербанк': 1473866,
                      'Банк ВТБ': 4181,
                      'Газпромнефть': 39305, 'Альфа-банк': 80, 'Offer Now': 9056230, 'ФинТех IQ': 5898393,
                      'КНОПКАДЕНЬГИ': 4968470}

    data = []

    for company_name, company_id in companies_data.items():
        company_url = f"https://hh.ru/employer/{company_id}"
        company_info = {'company_id': company_id, 'company_name': company_name, 'company_url': company_url}
        data.append(company_info)

    return data


def get_vacancies(data):
    """
    Получает информацию о вакансиях для компаний из предоставленного списка.

    :param data: Список словарей с информацией о компаниях.
    :type data: list[dict]
    :return: Список словарей с информацией о вакансиях для каждой компании.
    :rtype: list[dict]
    """
    vacancies_info = []
    for company_data in data:
        company_id = company_data['company_id']
        url = f"https://api.hh.ru/vacancies?employer_id={company_id}"
        response = requests.get(url)
        if response.status_code == 200:
            vacancies = response.json()['items']
            vacancies_info.extend(vacancies)
        else:
            print(f"Ошибка при запросе к API для компании {company_data['company_name']}: {response.status_code}")
    return vacancies_info


def get_vacancies_list(data):
    """
    Преобразует информацию о вакансиях в формат, подходящий для сохранения в базе данных.

    :param data: Список словарей с информацией о вакансиях.
    :type data: list[dict]
    :return: Список словарей с данными, подходящими для сохранения в БД.
    :rtype: list[dict]
    """
    vacancies = []
    for item in data:
        company_id = item['employer']['id']
        company = item['employer']['name']
        company_url = item['employer']['url']
        job_title = item['name']
        link_to_vacancy = item['alternate_url']
        salary = item['salary']
        currency = ''
        salary_from = 0
        if salary:
            salary_from = salary['from'] if salary['from'] is not None else 0
            currency = salary['currency'] if salary['currency'] is not None else ''
        description = item['snippet']['responsibility']
        requirement = item['snippet']['requirement']
        vacancies.append(
            {"company_id": company_id, "company_name": company, "company_url": company_url, "job_title": job_title,
             "link_to_vacancy": link_to_vacancy, "salary_from": salary_from, "currency": currency,
             "description": description, "requirement": requirement})
    return vacancies
