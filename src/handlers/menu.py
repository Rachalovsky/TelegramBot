from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram_patch.router import Router
from src.tools.filters import is_register_user

menu_router = Router()


@menu_router.on_message(filters.command('start') & filters.private & is_register_user)
def say_hi(bot: Client, message: Message):
    bot.send_message(message.chat.id, "Hi, I'm working")

