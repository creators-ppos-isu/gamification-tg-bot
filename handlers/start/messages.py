from dataclasses import dataclass


WELCOME = 'Привет 👋' \
          '\n\nЯ бот системы геймификации'


@dataclass
class Registration:
    START = 'Для продолжения необходимо зарегистрироваться!' \
            '\n\nОтправь свое имя и фамилию'

    COMPLETED = 'Регистрация успешно пройдена!'