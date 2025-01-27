import asyncio

from pyrogram import Client
from pyrogram_patch import patch
from pyrogram_patch.fsm.storages import MemoryStorage

import logging

from config import API_ID, API_HASH, TG_TOKEN
from handlers.registration import reg_router
from handlers.menu import menu_router
from handlers.tasks import task_router
from src.database.models import create_bd_tables


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
    patch_manager.include_router(reg_router)
    patch_manager.include_router(menu_router)
    patch_manager.include_router(task_router)
    await app.start()


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


