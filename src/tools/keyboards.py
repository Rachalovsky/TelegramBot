from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


MAIN_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton('➕ Добавить задачу', callback_data='create_new_task')],
    [InlineKeyboardButton('🎯 Актуальные задачи', callback_data='actual_user_tasks')],
    [InlineKeyboardButton('✅ Выполненные задачи', callback_data='completed_user_tasks')],
    [InlineKeyboardButton('❌ Удалить выполненное', callback_data='delete_completed_tasks')],
    [InlineKeyboardButton('📋 Все задачи', callback_data='all_user_tasks')],
])


async def get_task_menu(task_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('✅ Пометить как выполненную', callback_data=f'mark_task_done_{task_id}')],
        [InlineKeyboardButton('❌ Удалить задачу', callback_data=f'delete_task_{task_id}')],
        [InlineKeyboardButton('🏠 Главное меню', callback_data='main_menu')],
    ])


