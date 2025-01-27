from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram_patch.router import Router

bot_commands = Router()


@bot_commands.on_message(filters.command("about") & filters.private)
async def about_bot_handler(client: Client, message: Message) -> None:
    await client.send_message(
        chat_id=message.chat.id,
        text="👋 Привет! Я ваш персональный менеджер задач. "
             "Моя цель - помочь вам организовать свои дела и упростить управление задачами.\n\n"
             "Вот что я могу для вас сделать:\n\n"
             "➕ **Создание задач**: Легко добавляйте новые задачи и управляйте ими.\n"
             "✅ **Отслеживание выполнения**: Помечайте задачи как выполненные, чтобы отслеживать свой прогресс.\n"
             "📋 **Просмотр задач**: Получайте быстрый доступ к списку актуальных и выполненных задач.\n"
             "❌ **Удаление задач**: Удаляйте завершенные задачи для поддержания чистоты списка.\n\n"
             "Чтобы начать, нажмите на кнопку /start!"
    )


@bot_commands.on_message(filters.command("code") & filters.private)
async def code_handler(client: Client, message: Message) -> None:
    await client.send_message(
        chat_id=message.chat.id,
        text="Исходный код моего приложения доступен на GitHub. Вы можете ознакомиться с ним по ссылке ниже:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Посетить GitHub репозиторий",
                                  url="https://github.com/Rachalovsky/TelegramBot/")]
        ])
    )
