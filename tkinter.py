import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

import psycopg2

from src.config import config
from src.db_manager import DBManager
from src.get_vacancy import get_vacancies_list, get_companies, get_vacancies
from src.utils import create_db, insert_data

# Получение параметров конфигурации
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

# Инициализация менеджера базы данных
db_manager = DBManager("best_vacancies", params)


def display_results(title, results):
    """Отображает результаты в отдельном окне с возможностью копирования."""
    result_window = tk.Toplevel()
    result_window.title(title)

    text = tk.Text(result_window)
    text.pack(expand=True, fill=tk.BOTH)

    for result in results:
        text.insert(tk.END, f"{result}\n")

    # Добавляем кнопку для копирования текста
    copy_button = ttk.Button(result_window, text="Копировать",
                             command=lambda: result_window.clipboard_append(text.get("1.0", tk.END)))
    copy_button.pack()


def show_companies_and_vacancies_count():
    """Показать компании и количество вакансий."""
    companies_vacancies_count = db_manager.get_companies_and_vacancies_count()
    display_results("Список всех компаний и количество вакансий у каждой компании", companies_vacancies_count.items())


def show_all_vacancies():
    """Показать всё вакансии."""
    vacancy_list = db_manager.get_all_vacancies()
    display_results("Список всех вакансий", vacancy_list)


def show_avg_salary():
    """Показать среднюю зарплату."""
    avg_salary = db_manager.get_avg_salary()
    messagebox.showinfo("Средняя зарплата по вакансиям", f"Средняя зарплата по вакансиям: {avg_salary}")


def show_vacancies_with_higher_salary():
    """Показать вакансии с зарплатой выше средней."""
    vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
    display_results("Вакансии с зарплатой выше средней", vacancies_with_higher_salary)


def show_vacancies_with_keyword():
    """Показать вакансии с заданным ключевым словом."""
    keyword = simpledialog.askstring("Введите слово", "Введите слово:")
    if keyword:
        vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
        display_results(f"Вакансии с ключевым словом '{keyword}'", vacancies_with_keyword)


def main():
    """Основная функция, создающая главное окно приложения."""
    root = tk.Tk()
    root.title("Вакансии")

    tk.Button(root, text="Список всех компаний и количество вакансий у каждой компании",
              command=show_companies_and_vacancies_count).pack(fill=tk.X)
    tk.Button(root, text="Список всех вакансий", command=show_all_vacancies).pack(fill=tk.X)
    tk.Button(root, text="Средняя зарплата по вакансиям", command=show_avg_salary).pack(fill=tk.X)
    tk.Button(root, text="Вакансии с зарплатой выше средней", command=show_vacancies_with_higher_salary).pack(fill=tk.X)
    tk.Button(root, text="Вакансии с заданным ключевым словом", command=show_vacancies_with_keyword).pack(fill=tk.X)
    tk.Button(root, text="Выход", command=root.quit).pack(fill=tk.X)

    root.mainloop()


if __name__ == "__main__":
    main()
