from aiogram import Router, F
from aiogram.types import Message
from tortoise.exceptions import DoesNotExist

from db.models.user import User


admin_router = Router()


@admin_router.message(F.web_app_data)
async def handle_web_app(message: Message): 
    user_id = message.web_app_data.data
    try: 
        user = await User.get(id=user_id)
    except DoesNotExist: 
        return await message.answer(f'Пользователь с индентификатором {user_id} не найден в системе!')
    
    await message.answer(f'Выберите задание для назначения быллов пользователю <b>{user}</b>')

