from pyrogram.types import Message

from pyrogram import filters
from database.models import async_session, User
from sqlalchemy import select


async def check_register_user(_, __, m: Message) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == m.from_user.id))
        return False if not user else True


async def check_unregister_user(_, __, m: Message) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == m.from_user.id))
        return True if not user else False


is_register_user = filters.create(check_register_user)
is_unregister_user = filters.create(check_unregister_user)
