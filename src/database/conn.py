from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import PG_USER, PG_PASSWORD, PG_DATABASE, PG_HOST, PG_PORT

DATABASE_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine)

