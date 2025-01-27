from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram_patch.fsm import StatesGroup, StateItem, State
from pyrogram_patch.fsm.filter import StateFilter

from pyrogram_patch.router import Router
from src.database.requests import *
from src.tools.filters import is_register_user
from src.tools.other import is_done_task
from src.tools.keyboards import get_task_menu
from src.handlers.menu import main_menu_callback_handler, main_menu_handler

task_router = Router()


class CreateTask(StatesGroup):
    """
    Класс для управления состояниями процесса создания задачи.

    Атрибуты:
        name (StateItem): Состояние для ввода названия задачи.
        description (StateItem): Состояние для ввода описания задачи.
        owner_id (StateItem): Состояние для хранения идентификатора владельца задачи.
    """
    name = StateItem()
    description = StateItem()
    owner_id = StateItem()

    @staticmethod
    def validate_name(value: str) -> bool:
        """
        Валидирует название задачи.

        Аргументы:
            value (str): Название задачи.

        Возвращает:
            bool: True, если название задачи валидно, иначе False.
        """
        if len(value) <= 50:
            return True
        return False

    @staticmethod
    def validate_description(value: str) -> bool:
        """
       Валидирует описание задачи.

       Аргументы:
           value (str): Описание задачи.

       Возвращает:
           bool: True, если описание задачи валидно, иначе False.
       """
        if len(value) <= 250:
            raise True
        return False

    async def on_name_set(self, value: str) -> None:
        """
        Устанавливает значение названия задачи, если оно валидно.

        Аргументы:
            value (str): Название задачи.

        Исключения:
            ValueError: Если название задачи не валидно.
        """
        if not self.validate_name(value):
            raise ValueError("Название задачи не должно превышать 50 символов.")

    async def on_description_set(self, value: str) -> None:
        """
        Устанавливает значение описания задачи, если оно валидно.

        Аргументы:
            value (str): Описание задачи.

        Исключения:
            ValueError: Если описание задачи не валидно.
        """
        if not self.validate_description(value):
            raise ValueError("Описание задачи не должно превышать 250 символов.")


@task_router.on_callback_query(filters.regex('create_new_task'))
async def start_create_task(client: Client, callback: CallbackQuery, state: State) -> None:
    """
    Обработчик колбэка для начала создания новой задачи.

    Аргументы:
        client (Client): Клиент Pyrogram.
        callback (CallbackQuery): Колбэк, вызвавший хэндлер.
        state (State): Состояние FSM.

    Операции:
        - Отправляет сообщение с запросом названия задачи.
        - Устанавливает состояние на CreateTask.name.
    """
    await client.send_message(chat_id=callback.message.chat.id,
                              text='Давайте создадим новую задачу! \n'
                                   'Пожалуйста, введите название задачи:')
    await state.set_state(CreateTask.name)


@task_router.on_message(filters.private & StateFilter(CreateTask.name) & is_register_user)
async def process_task_name(client: Client, message: Message, state: State) -> None:
    """
    Обработчик для состояния CreateTask.name.

    Аргументы:
        client (Client): Клиент Pyrogram.
        message (Message): Сообщение, вызвавшее хэндлер.
        state (State): Состояние FSM.

    Операции:
        - Валидирует название задачи.
        - Сохраняет название задачи и идентификатор владельца.
        - Запрашивает описание задачи.
        - Устанавливает состояние на CreateTask.description.
    """
    name_valid = False

    while not name_valid:
        try:
            create_task_inst = CreateTask()
            await create_task_inst.on_name_set(message.text)
            name_valid = True
        except ValueError as e:
            await message.reply(str(e))
            return

    owner_id = await get_user_id_by_tg_id(message.from_user.id)
    await state.set_data({'owner_id': owner_id})
    await state.set_data({'name': message.text})
    await client.send_message(message.chat.id, "Пожалуйста, введите описание задачи:")
    await state.set_state(CreateTask.description)


@task_router.on_message(filters.private & StateFilter(CreateTask.description) & is_register_user)
async def process_task_description(client: Client, message: Message, state: State) -> None:
    """
    Обработчик для состояния CreateTask.description.

    Аргументы:
        client (Client): Клиент Pyrogram.
        message (Message): Сообщение, вызвавшее хэндлер.
        state (State): Состояние FSM.

    Операции:
        - Валидирует описание задачи.
        - Сохраняет описание задачи.
        - Добавляет задачу в базу данных.
        - Отправляет сообщение об успешном создании задачи.
        - Возвращает пользователя в главное меню.
    """
    description_valid = False

    while not description_valid:
        try:
            create_task_inst = CreateTask()
            await create_task_inst.on_description_set(message.text)
            description_valid = True
        except ValueError as e:
            print(e)
            await message.reply(str(e))
            return

    await state.set_data({'description': message.text})
    data = await state.get_data()
    try:
        await add_task(data)
    except Exception as e:
        print(e)

    await client.send_message(chat_id=message.chat.id,
                              text="Задача успешно создана!")
    await main_menu_handler(client, message)


@task_router.on_callback_query(filters.regex(r'^task_') & is_register_user)
async def get_task_handler(client: Client, callback: CallbackQuery):
    """
    Обработчик колбэка для получения информации о задаче.

    Аргументы:
        client (Client): Клиент Pyrogram.
        callback (CallbackQuery): Колбэк, вызвавший хэндлер.

    Операции:
        - Извлекает идентификатор задачи из данных колбэка.
        - Получает задачу из базы данных.
        - Обновляет сообщение с информацией о задаче и разметкой клавиатуры.
    """
    task_id = str(callback.data).split('_')[1]
    task = await get_task_by_id(int(task_id))

    await callback.edit_message_text(
        text=f'{await is_done_task(task.is_done)} - **{task.name}**\n\nОписание задачи:\n{task.description}',
        reply_markup=await get_task_menu(task.id)
    )


@task_router.on_callback_query(filters.regex(r'^mark_task_done_') & is_register_user)
async def mark_task_as_complete_handler(client: Client, callback: CallbackQuery):
    """
    Обработчик колбэка для пометки задачи как выполненной.

    Аргументы:
        client (Client): Клиент Pyrogram.
        callback (CallbackQuery): Колбэк, вызвавший хэндлер.

    Операции:
        - Извлекает идентификатор задачи из данных колбэка.
        - Помечает задачу как выполненную в базе данных.
        - Отправляет уведомление об успешном выполнении задачи.
        - Обновляет информацию о задаче.
    """
    task_id = str(callback.data).split('_')[3]
    await mark_task_as_complete(int(task_id))

    await callback.answer("Задача Выполнена! ✅", show_alert=True)

    callback.data = f'task_{task_id}'
    await get_task_handler(client, callback)



@task_router.on_callback_query(filters.regex(r'^delete_task_') & is_register_user)
async def delete_task_handler(client: Client, callback: CallbackQuery):
    """
    Обработчик колбэка для удаления задачи.

    Аргументы:
        client (Client): Клиент Pyrogram.
        callback (CallbackQuery): Колбэк, вызвавший хэндлер.

    Операции:
        - Извлекает идентификатор задачи из данных колбэка.
        - Удаляет задачу из базы данных.
        - Отправляет уведомление об успешном удалении задачи.
        - Возвращает пользователя в главное меню.
    """
    task_id = str(callback.data).split('_')[2]
    await delete_task(int(task_id))

    await callback.answer("Задача Удалена ❌", show_alert=True)

    callback.data = 'main_menu'
    await main_menu_callback_handler(client, callback)
