import asyncio

from pyrogram import Client
from pyrogram_patch import patch
from pyrogram_patch.fsm.storages import MemoryStorage

import logging

from config import API_ID, API_HASH, TG_TOKEN
from handlers.registration import reg_router
from handlers.menu import menu_router
from src.database.models import create_bd_tables


async def main():
    await create_bd_tables()
    app = Client(name="ToDO_bot", api_id=API_ID, api_hash=API_HASH, bot_token=TG_TOKEN)
    patch_manager = patch(app)
    patch_manager.set_storage(MemoryStorage())
    patch_manager.include_router(reg_router)
    patch_manager.include_router(menu_router)
    await app.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(main())
        loop.run_forever()
    except KeyboardInterrupt:
        print("Остановка бота")
        loop.stop()
    finally:
        print("Бот остановлен")


