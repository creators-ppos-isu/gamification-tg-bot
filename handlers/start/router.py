from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from tortoise.exceptions import ValidationError

from db.models.user import User
from utils.qrcode import generate_qr_code_url
from utils.decorators import prefetch_user
from .states import RegistrationForm
from .messages import (
    WELCOME,
    Registration,
)
from .keyboards import get_main_menu_kb


start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user, created = await User.get_or_create(id=message.from_user.id)

    if created: 
        await state.set_state(RegistrationForm.full_name)
        return await message.answer(Registration.START)

    keyboard = get_main_menu_kb(user)

    return await message.answer(WELCOME, reply_markup=keyboard)


@start_router.message(RegistrationForm.full_name)
async def proccess_full_name(message: Message, state: FSMContext): 
    user = await User.get(id=message.from_user.id)

    try: 
        first_name, last_name = message.text.split()
    except ValueError:
        return await message.answer('Ты должен отправить только свои имя и фамилию')

    user.first_name = first_name
    user.last_name = last_name

    try:
        await user.save()
    except ValidationError as e:
        return await message.answer(str(e))

    keyboard = get_main_menu_kb(user)

    await message.answer(Registration.COMPLETED, reply_markup=keyboard)
    await state.clear()


@start_router.message(F.text == 'Задания')
@prefetch_user
async def send_tasks(message: Message, user: User):
    await message.answer('Задания')


@start_router.message(F.text == 'Профиль')
@prefetch_user
async def send_profile(message: Message, user: User):
    content = f'<b>Профиль</b>' \
              f'\n\nИмя: {user.first_name}' \
              f'\nФамилия: {user.last_name}' \
              f'\nБаллы: {user.score}'
    await message.answer_photo(
        photo=generate_qr_code_url(data=user.id),
        caption=content
    )
