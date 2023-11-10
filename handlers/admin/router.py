from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tortoise.exceptions import DoesNotExist

from db.models.user import User
from db.models.task import Task
from .messages import Error, Menu


admin_router = Router()


class SelectTaskCallback(CallbackData, prefix='task'):
    user_id: int
    task_id: int


@admin_router.message(F.web_app_data)
async def handle_web_app(message: Message): 
    user_id = message.web_app_data.data

    try: 
        user = await User.get(id=user_id)
    except DoesNotExist: 
        return await message.answer(Error.USER_NOT_FOUND.format(user_id=user_id))

    tasks = await Task.all()

    builder = InlineKeyboardBuilder()
    for task in tasks: 
        builder.button(
            text=task.title, 
            callback_data=SelectTaskCallback(
                task_id=task.id, 
                user_id=user.id
            )
        )
    builder.adjust(1)
    keyboard = builder.as_markup()

    await message.answer(text=Menu.SELECT_TASK.format(user=user), reply_markup=keyboard)


@admin_router.callback_query(SelectTaskCallback.filter())
async def select_task_callback(query: CallbackQuery, callback_data: SelectTaskCallback): 
    task = await Task.get(id=callback_data.task_id)
    user = await User.get(id=callback_data.user_id)

    await user.completed_task.add(task)
    user.score += task.score
    await user.save()

    await query.message.answer(f'Успешно добавленно {task.score} баллов пользователю {user} за {task.title}')

