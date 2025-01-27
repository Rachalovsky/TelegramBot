import re

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram_patch.fsm import StatesGroup, StateItem, State
from pyrogram_patch.fsm.filter import StateFilter

from pyrogram_patch.router import Router
from src.database.requests import *
from src.tools.filters import is_unregister_user
from sqlalchemy.exc import IntegrityError

reg_router = Router()


class Registration(StatesGroup):
    """
    Класс для управления состояниями процесса регистрации.

    Атрибуты:
        name (StateItem): Состояние для ввода имени пользователя.
        login (StateItem): Состояние для ввода логина пользователя.
    """
    name = StateItem()
    login = StateItem()

    @staticmethod
    def validate_name(value: str) -> bool:
        if len(value) <= 25:
            return True
        return False

    @staticmethod
    def validate_login(value: str) -> bool:
        pattern = r'^[a-zA-Z0-9._]+$'
        if re.match(pattern, value) and len(value) <= 25:
            return True
        return False

    async def on_name_set(self, value: str) -> None:
        if not self.validate_name(value):
            raise ValueError("Название задачи не должно превышать 25 символов.")

    async def on_login_set(self, value: str) -> None:
        if not self.validate_login(value):
            raise ValueError(f"Логин '{value}' невалиден.\n"
                             f"Допустимы только латинские буквы, цифры, подчеркивания и точки.\n"
                             f"Максимальное допустимое кол-во символов 25.")


@reg_router.on_message(filters.command("start") & filters.private & is_unregister_user)
async def start_reg_handler(client: Client, message: Message, state: State) -> None:
    """
    Обработчик команды /start для незарегистрированных пользователей.

    Аргументы:
        client (Client): Клиент Pyrogram.
        message (Message): Сообщение, вызвавшее команду.
        state (State): Состояние FSM.

    Операции:
        - Отправляет сообщение с запросом имени пользователя.
        - Устанавливает состояние на Registration.name.
    """
    await client.send_message(chat_id=message.chat.id,
                              text='Привет! 🎉 Это твой персональный менеджер задач!\n'
                                   'Чтобы начать пользоваться ботом,пожалуйста, пройдите небольшую регистрацию. '
                                   'Это займет меньше минуты. 😊\n\nПожалуйста, введите своё имя:')
    await state.set_state(Registration.name)


@reg_router.on_message(filters.private & StateFilter(Registration.name) & is_unregister_user)
async def process_name(client: Client, message: Message, state: State) -> None:
    """
    Обработчик для состояния Registration.name.

    Аргументы:
        client (Client): Клиент Pyrogram.
        message (Message): Сообщение, вызвавшее команду.
        state (State): Состояние FSM.

    Операции:
        - Валидирует имя пользователя.
        - Сохраняет имя пользователя.
        - Запрашивает логин пользователя.
        - Устанавливает состояние на Registration.login.
    """
    name_valid = False

    while not name_valid:
        try:
            registration_instance = Registration()
            await registration_instance.on_name_set(message.text)
            name_valid = True
        except ValueError as e:
            await message.reply(str(e))
            return

    await state.set_data({'name': message.text})
    await client.send_message(message.chat.id, "Пожалуйста, придумайте уникальный никнейм:")
    await state.set_state(Registration.login)


@reg_router.on_message(filters.private & StateFilter(Registration.login) & is_unregister_user)
async def process_login(client: Client, message: Message, state: State) -> None:
    """
    Обработчик для состояния Registration.login.

    Аргументы:
        client (Client): Клиент Pyrogram.
        message (Message): Сообщение, вызвавшее команду.
        state (State): Состояние FSM.

    Операции:
        - Валидирует логин пользователя.
        - Сохраняет логин и идентификатор Telegram пользователя.
        - Добавляет пользователя в базу данных.
        - Отправляет сообщение об успешной регистрации.
    """
    login_valid = False

    while not login_valid:
        try:
            registration_instance = Registration()
            await registration_instance.on_login_set(message.text)
            login_valid = True
        except ValueError as e:
            await message.reply(str(e))
            return

    await state.set_data({'login': message.text})
    data = await state.get_data()
    data['tg_id'] = message.from_user.id
    try:
        await add_user(data)
    except IntegrityError as e:
        await client.send_message(chat_id=message.chat.id,
                                  text='Данный никнейм уже занят, попробуйте снова:')
    else:
        await client.send_message(chat_id=message.chat.id,
                                  text=f"Поздравляем, {data['name']}!\n"
                                       f"Вы успешно зарегистрированы.🎉\n"
                                       f"Ваш логин: {data['login']}")
        await state.finish()


@reg_router.on_message(filters.private & is_unregister_user)
async def hint(client: Client, message: Message) -> None:
    """
    Обработчик для всех сообщений от незарегистрированных пользователей.

    Аргументы:
        client (Client): Клиент Pyrogram.
        message (Message): Сообщение, вызвавшее команду.

    Операции:
        - Отправляет подсказку для начала регистрации.
    """
    await client.send_message(message.from_user.id, "Для начала регистрации введите /start")


