from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from db.models.user import User


def get_main_menu_kb(user: User):
    builder = ReplyKeyboardBuilder()

    builder.button(text='Задания')
    builder.button(text='Профиль')

    if user.is_admin:
        builder.button(
            text='QR сканнер', 
            web_app=WebAppInfo(url='https://bitcoinschool.su/data/index.html')
        )

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)