import psycopg2

from src.get_vacancy import get_vacancies, get_companies, get_vacancies_list

data = get_vacancies(get_companies())
vacancies = get_vacancies_list(data)


def create_db(name: str, params: dict) -> str:
    """
    СозБД и таблицы для сохранения данных о компаниях и вакансиях.

    :param name: Имя создаваемой базы данных.
    :type name: str
    :param params: Параметры подключения к базе данных (например, пользователь, пароль, хост).
    :type params: dict
    :return: Сообщение об успешном создании базы данных и таблиц или об ошибке.
    :rtype: str
    """
    try:
        # Подключение к основной базе данных для создания новой БД
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f'DROP DATABASE IF EXISTS {name}')
        cur.execute(f'CREATE DATABASE {name}')
        conn.close()

        # Подключение к новой базе данных и создание таблиц
        conn = psycopg2.connect(dbname=name, **params)
        with conn.cursor() as cur:
            cur.execute('''CREATE TABLE IF NOT EXISTS employers (
                           company_id INT PRIMARY KEY, 
                           company_name VARCHAR(100), 
                           company_url VARCHAR(100))''')
        with conn.cursor() as cur:
            cur.execute('''CREATE TABLE IF NOT EXISTS vacancies (
                           company_name VARCHAR(100), 
                           job_title VARCHAR(100), 
                           link_to_vacancy VARCHAR(100), 
                           salary_from INT, 
                           currency VARCHAR(10), 
                           description TEXT, 
                           requirement TEXT)''')
        conn.commit()
        conn.close()

        return "База данных и таблицы успешно созданы."

    except Exception as e:
        return f"Произошла ошибка: {e}"


def insert_data(conn, vacancy: list[dict]) -> None:
    """
    Сохраняет данные о компаниях и вакансиях в БД.

    :param conn: Подключение к базе данных.
    :type conn: psycopg2.extensions.connection
    :param vacancy: Список словарей с информацией о вакансиях.
    :type vacancy: list[dict]
    """
    insert_employer_query = """
    INSERT INTO employers (company_id, company_name, company_url) 
    VALUES (%s, %s, %s)
    ON CONFLICT (company_id) DO NOTHING
    """
    insert_vacancy_query = """
    INSERT INTO vacancies (company_name, job_title, link_to_vacancy, salary_from, currency, description, requirement)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        with conn.cursor() as cur:
            for record in vacancy:
                cur.execute(insert_employer_query,
                            (record['company_id'], record['company_name'], record['company_url']))
                cur.execute(insert_vacancy_query, (
                    record['company_name'], record['job_title'], record['link_to_vacancy'], record['salary_from'],
                    record['currency'], record['description'], record['requirement']))
            conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Произошла ошибка при вставке данных: {e}")
    finally:
        conn.close()
