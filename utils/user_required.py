from aiogram.types import Message
from tortoise.exceptions import DoesNotExist
from db.models.user import User


def user_required(fn): 
    async def wrapper(message: Message):
        try:
            user = await User.get(id=message.from_user.id)
        except DoesNotExist: 
            return await message.answer(f'Пользователь {message.from_user.id} не найден!')
        return await fn(message, user)
    return wrapper