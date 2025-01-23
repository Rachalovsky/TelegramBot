from typing import List
from datetime import datetime

from sqlalchemy import BigInteger, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.conn import Base, engine


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(25))
    login: Mapped[str] = mapped_column(String(25))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    update_at: Mapped[datetime] = mapped_column(DateTime,
                                                default=datetime.now(),
                                                onupdate=datetime.now())

    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="owner", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)
    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(120))
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    update_at: Mapped[datetime] = mapped_column(DateTime,
                                                default=datetime.now(),
                                                onupdate=datetime.now())

    owner: Mapped["User"] = relationship("User", back_populates="tasks")



async def create_bd_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


