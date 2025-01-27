import asyncio
import logging
from pyrogram import Client
from pyrogram.types import BotCommand
from pyrogram_patch import patch
from pyrogram_patch.fsm.storages import MemoryStorage

from src.config import API_ID, API_HASH, TG_TOKEN
from src.handlers.registration import reg_router
from src.handlers.menu import menu_router
from src.handlers.tasks import task_router
from src.handlers.bot_commands import bot_commands
from src.database.models import create_bd_tables


async def set_bot_commands(client: Client):
    await client.set_bot_commands([
        BotCommand("start", "Запустить менеджер задач"),
        BotCommand("about", "Информация о боте"),
        BotCommand("code", "Ссылка на GitHub")
    ])


def include_routers(patch_manager, *routers):
    for router in routers:
        patch_manager.include_router(router)


async def main():
    """
    Главная асинхронная функция для запуска бота.

    Операции:
        - Создает таблицы базы данных, если они еще не существуют.
        - Инициализирует клиент Pyrogram с заданными параметрами.
        - Патчит клиент для работы с состояниями.
        - Устанавливает хранилище для состояний в памяти.
        - Подключает маршрутизаторы для регистрации, меню и задач.
        - Запускает клиент Pyrogram.

    Примечание:
        Убедитесь, что переменные API_ID, API_HASH и TG_TOKEN заданы корректно и доступны в контексте выполнения.
    """
    await create_bd_tables()
    app = Client(name="ToDO_bot", api_id=API_ID, api_hash=API_HASH, bot_token=TG_TOKEN)
    patch_manager = patch(app)
    patch_manager.set_storage(MemoryStorage())
    include_routers(patch_manager, bot_commands, reg_router, menu_router, task_router)
    await app.start()
    await set_bot_commands(app)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    try:
        print('Бот запускается. Пожалуйста, подождите...')
        loop.create_task(main())
        loop.run_forever()
    except KeyboardInterrupt:
        print("Остановка бота. Завершаем все текущие задачи...")
        loop.stop()
    finally:
        print("Бот успешно остановлен. До новых встреч!")
