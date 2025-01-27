from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DATABASE)

DATABASE_URL = (f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
                f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}")

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine)
