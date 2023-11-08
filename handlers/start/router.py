from aiogram import Router, F
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import CommandStart

from db.models.user import User
from utils import qrcode
from utils.user_required import user_required


start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user, _ = await User.get_or_create(id=message.from_user.id)

    builder = ReplyKeyboardBuilder()

    if user.is_admin:
        builder.button(text='QR сканнер', web_app=WebAppInfo(url='https://bitcoinschool.su/data/'))
    else: 
        builder.button(text='Задания')
        builder.button(text='Профиль')

    builder.adjust(1)
    keyboard = builder.as_markup(resize_keyboard=True)

    await message.answer('Привет 👋\n\nЯ бот системы геймификации', reply_markup=keyboard)

# todo Реализация регистрации

@start_router.message(F.text == 'Задания')
@user_required
async def send_tasks(message: Message, user: User):
    await message.answer('Задания')


@start_router.message(F.text == 'Профиль')
@user_required
async def send_profile(message: Message, user: User): 
    await message.answer_photo(
        photo=qrcode.generate_qr_code_url(data=user.id),
        caption='Профиль'
    )
