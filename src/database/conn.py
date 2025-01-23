from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker

from config import PG_USER, PG_PASSWORD, PG_DATABASE, PG_HOST, PG_PORT

DATABASE_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def create_bd_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
