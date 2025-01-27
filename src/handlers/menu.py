from pyrogram import filters, Client
from pyrogram.types import Message, CallbackQuery
from pyrogram_patch.router import Router
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.tools.keyboards import MAIN_MENU
from src.tools.filters import is_register_user
from src.tools.other import is_done_task
from src.database.requests import (get_all_tasks_list, get_actual_tasks_list, get_completed_tasks_list,
                                   delete_completed_tasks)

menu_router = Router()


@menu_router.on_message(filters.command("start") & filters.private & is_register_user)
async def main_menu_handler(client: Client, message: Message) -> None:
    """
    Обработчик команды /start для зарегистрированных пользователей.

    Аргументы:
        client (Client): Клиент Pyrogram.
        message (Message): Сообщение, вызвавшее команду.

    Операции:
        - Отправляет сообщение с основным меню, используя клавиатуру MAIN_MENU.
    """
    await message.reply(
        text="Выберите пункт меню",
        reply_markup=MAIN_MENU
    )


@menu_router.on_callback_query(filters.regex("main_menu") & is_register_user)
async def main_menu_callback_handler(client: Client, callback: CallbackQuery) -> None:
    """
    Обработчик колбэка для главного меню.

    Аргументы:
        client (Client): Клиент Pyrogram.
        callback (CallbackQuery): Колбэк, вызвавший хэндлер.

    Операции:
        - Обновляет сообщение с главным меню, используя клавиатуру MAIN_MENU.
    """
    if callback.data == 'main_menu':
        await callback.edit_message_text(
            text="Главное меню",
            reply_markup=MAIN_MENU
        )


@menu_router.on_callback_query(filters.regex('actual_user_tasks') & is_register_user)
async def get_actual_tasks_handler(client: Client, callback: CallbackQuery) -> None:
    """
    Обработчик колбэка для получения списка актуальных (невыполненных) задач пользователя.

    Аргументы:
        client (Client): Клиент Pyrogram.
        callback (CallbackQuery): Колбэк, вызвавший хэндлер.

    Операции:
        - Получает список актуальных задач пользователя.
        - Создает клавиатуру с задачами и кнопкой возврата в главное меню.
        - Обновляет сообщение с разметкой клавиатуры.
    """
    tasks = await get_actual_tasks_list(callback.from_user.id)

    keyboard = [[InlineKeyboardButton(text=f'{await is_done_task(task.is_done)} - {task.name}',
                                      callback_data=f'task_{task.id}')] for task in tasks]
    keyboard.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data='main_menu')])

    await callback.edit_message_text(
        text='Ваш список актуальных задач',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


@menu_router.on_callback_query(filters.regex('completed_user_tasks') & is_register_user)
async def get_completed_tasks_handler(client: Client, callback: CallbackQuery) -> None:
    """
    Обработчик колбэка для получения списка выполненных задач пользователя.

    Аргументы:
        client (Client): Клиент Pyrogram.
        callback (CallbackQuery): Колбэк, вызвавший хэндлер.

    Операции:
        - Получает список выполненных задач пользователя.
        - Создает клавиатуру с задачами и кнопкой возврата в главное меню.
        - Обновляет сообщение с разметкой клавиатуры.
    """
    tasks = await get_completed_tasks_list(callback.from_user.id)

    keyboard = [[InlineKeyboardButton(text=f'{await is_done_task(task.is_done)} - {task.name}',
                                      callback_data=f'task_{task.id}')] for task in tasks]
    keyboard.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data='main_menu')])

    await callback.edit_message_text(
        text='Ваш список выполненных задач',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


@menu_router.on_callback_query(filters.regex('all_user_tasks') & is_register_user)
async def get_all_tasks_handler(client: Client, callback: CallbackQuery) -> None:
    """
    Обработчик колбэка для получения списка всех задач пользователя.

    Аргументы:
        client (Client): Клиент Pyrogram.
        callback (CallbackQuery): Колбэк, вызвавший хэндлер.

    Операции:
        - Получает список всех задач пользователя.
        - Создает клавиатуру с задачами и кнопкой возврата в главное меню.
        - Обновляет сообщение с разметкой клавиатуры.
    """
    tasks = await get_all_tasks_list(callback.from_user.id)

    keyboard = [[InlineKeyboardButton(text=f'{await is_done_task(task.is_done)} - {task.name}',
                                      callback_data=f'task_{task.id}')] for task in tasks]
    keyboard.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data='main_menu')])

    await callback.edit_message_text(
        text='Все ваши задачи',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


@menu_router.on_callback_query(filters.regex('delete_completed_tasks') & is_register_user)
async def delete_completed_tasks_handler(client: Client, callback: CallbackQuery) -> None:
    """
    Обработчик колбэка для удаления всех выполненных задач пользователя.

    Аргументы:
        client (Client): Клиент Pyrogram.
        callback (CallbackQuery): Колбэк, вызвавший хэндлер.

    Операции:
        - Удаляет все выполненные задачи пользователя.
        - Отправляет уведомление об успешном удалении задач.
    """
    await delete_completed_tasks(callback.from_user.id)
    await callback.answer("Выполненные задачи удалены ❌", show_alert=True)
