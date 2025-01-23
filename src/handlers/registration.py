from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram_patch.fsm import StatesGroup, StateItem, State
from pyrogram_patch.fsm.filter import StateFilter

from pyrogram_patch.router import Router
from src.database.requests import *
from src.tools.filters import is_unregister_user

reg_router = Router()


class Registration(StatesGroup):
    name = StateItem()
    login = StateItem()


@reg_router.on_message(filters.command("start") & filters.private & is_unregister_user)
async def start_reg_handler(client: Client, message: Message, state: State) -> None:
    await client.send_message(chat_id=message.chat.id,
                              text='Привет! 🎉 Это твой персональный менеджер задач!\n'
                                   'Чтобы начать пользоваться ботом,пожалуйста, пройдите небольшую регистрацию. '
                                   'Это займет меньше минуты. 😊\n\nПожалуйста, введите своё имя:')
    await state.set_state(Registration.name)


@reg_router.on_message(filters.private & StateFilter(Registration.name) & is_unregister_user)
async def process_name(client: Client, message: Message, state: State) -> None:
    await state.set_data({'name': message.text})
    await client.send_message(message.chat.id, "Пожалуйста, придумайте уникальный никнейм")
    await state.set_state(Registration.login)


@reg_router.on_message(filters.private & StateFilter(Registration.login) & is_unregister_user)
async def process_login(client: Client, message: Message, state: State) -> None:
    await state.set_data({'login': message.text})
    data = await state.get_data()
    await add_user(message.from_user.id, data)

    await client.send_message(chat_id=message.chat.id,
                              text=f"Поздравляем, {data['name']}!\n"
                                   f"Вы успешно зарегистрированы.🎉\n"
                                   f"Ваш логин: {data['login']}")
    await state.finish()


@reg_router.on_message(filters.private & is_unregister_user)
async def hint(client: Client, message: Message) -> None:
    await client.send_message(message.from_user.id, "Для начала регистрации введите /start")


