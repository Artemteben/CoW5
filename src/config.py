from configparser import ConfigParser
from typing import Dict


def config(filename: str = "database.ini", section: str = "postgresql") -> Dict[str, str]:
    """
    Читает параметры конфигурации базы данных из INI-файла и возвращает их в виде словаря.

    :param filename: Имя конфигурационного файла. По умолчанию "database.ini".
    :type filename: str, optional
    :param section: Название секции в конфигурационном файле, содержащей параметры подключения к базе данных.
    По умолчанию "postgresql".
    :type section: str, optional
    :return: Словарь с параметрами подключения к базе данных.
    :rtype: dict
    :raises FileNotFoundError: Если конфигурационный файл не найден.
    :raises KeyError: Если указанный раздел не найден в конфигурационном файле.
    """
    parser = ConfigParser()

    # Проверка на существование файла
    try:
        with open(filename, 'r') as file:
            parser.read_file(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден.")

    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise KeyError(f"Раздел '{section}' не найден в файле {filename}.")

    return db
