from sqlalchemy import select
from src.database.conn import async_session
from src.database.models import User, Task


async def add_user(tg_id, data):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(
                tg_id=tg_id,
                name=data['name'],
                login=data['login']
            ))
            await session.commit()
