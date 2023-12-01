from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tortoise.exceptions import DoesNotExist

from db.models.user import User, UserTask
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

    if await user.completed_task.filter(id=task.id).count() * task.score >= task.max_score:
        return await query.message.answer(
            f'Пользователю <b>{user}</b> нельзя добавить за задание <b>{task.title}</b> больше <b>{task.max_score}</b>'
            f' баллов'
        )

    await UserTask.create(task=task, user=user)
    user.score += task.score
    await user.save()

    await query.message.edit_text(
        f'Успешно добавлено <b>{task.score}</b> баллов пользователю <b>{user}</b> за задание <b>{task.title}</b>'
    )
    await query.bot.send_message(chat_id=user.id, text=f'Добавлены баллы {task.score} за задание <b>{task.title}</b> 🎉')
