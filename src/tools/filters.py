from pyrogram import filters
from pyrogram.types import Message
from sqlalchemy import select

from src.database.conn import async_session
from src.database.models import User


async def check_register_user(_, __, m: Message) -> bool:
    """
    Проверяет, зарегистрирован ли пользователь.

    Аргументы:
        _ (Any): Игнорируемый аргумент.
        __ (Any): Игнорируемый аргумент.
        m (Message): Сообщение, вызвавшее проверку.

    Возвращает:
        bool: True, если пользователь зарегистрирован, иначе False.
    """
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == m.from_user.id))
        return False if not user else True


async def check_unregister_user(_, __, m: Message) -> bool:
    """
    Проверяет, не зарегистрирован ли пользователь.

    Аргументы:
        _ (Any): Игнорируемый аргумент.
        __ (Any): Игнорируемый аргумент.
        m (Message): Сообщение, вызвавшее проверку.

    Возвращает:
        bool: True, если пользователь не зарегистрирован, иначе False.
    """
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == m.from_user.id))
        return True if not user else False


is_register_user = filters.create(check_register_user)
is_unregister_user = filters.create(check_unregister_user)
