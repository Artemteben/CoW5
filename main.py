import psycopg2

from src.config import config
from src.db_manager import DBManager
from src.get_vacancy import get_vacancies_list, get_companies, get_vacancies
from src.utils import create_db, insert_data

# Получение параметров конфигурации1
params = config()

# Получение данных о вакансиях
data = get_vacancies(get_companies())
vacancies = get_vacancies_list(data)

# Создание базы данных и таблиц
create_db('best_vacancies', params)

# Подключение к созданной базе данных
conn = psycopg2.connect(dbname='best_vacancies', **params)

# Вставка данных о вакансиях в БД
insert_data(conn, vacancies)


def main():
    """
    Основная функция, которая управляет взаимодействием с пользователем для выполнения запросов к базе данных.
    """
    # Инициализация менеджера базы данных
    db_manager = DBManager("best_vacancies", config())

    while True:
        print(f'Выберите запрос либо введите слово "стоп": \n'
              f'1 - Список всех компаний и количество вакансий у каждой компании\n'
              f'2 - Cписок всех вакансий с указанием названия компании, '
              f'названия вакансии, зарплаты и ссылки на вакансию\n'
              f'3 - Средняя зарплата по вакансиям\n'
              f'4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
              f'5 - Список всех вакансий, в названии которых содержится запрашиваемое слово\n')

        user_request = input()

        if user_request == '1':
            companies_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print(f"Список всех компаний и количество вакансий у каждой компании: {companies_vacancies_count}")
        elif user_request == '2':
            vacancy_list = db_manager.get_all_vacancies()
            print(
                f"Список всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию: "
                f"{vacancy_list}")
        elif user_request == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {avg_salary}")
        elif user_request == '4':
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print(
                f"Список всех вакансий, у которых зарплата выше средней по всем вакансиям:"
                f" {vacancies_with_higher_salary}")
        elif user_request == '5':
            user_input = input(f'Введите слово: ')
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_input)
            print(f"Список всех вакансий, в названии которых содержится '{user_input}': {vacancies_with_keyword}")
        elif user_request == 'стоп':
            break
        else:
            print("Введён неверный запрос")


if __name__ == "__main__":
    main()
