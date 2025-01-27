from typing import List
from datetime import datetime
from sqlalchemy import BigInteger, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

from src.database.conn import engine


class Base(AsyncAttrs, DeclarativeBase):
    """
    Базовый класс для всех моделей, используемых в базе данных.

    Наследует:
    - AsyncAttrs: Асинхронные атрибуты для поддержки асинхронных операций.
    - DeclarativeBase: Декларативная основа для моделей SQLAlchemy.

    Примечание:
    Этот класс не содержит методов и атрибутов. Он используется в качестве базового
    класса для всех моделей базы данных.
    """
    pass


class User(Base):
    """
    Модель для таблицы пользователей.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя.
        tg_id (int): Идентификатор пользователя в Telegram.
        name (str): Имя пользователя, максимум 25 символов.
        login (str): Уникальный логин пользователя, максимум 25 символов.
        created_at (datetime): Дата и время создания пользователя.
        update_at (datetime): Дата и время последнего обновления данных пользователя.
        tasks (List[Task]): Список задач, связанных с пользователем.

    Связи:
        tasks: Один пользователь может иметь несколько задач.
    """
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(25))
    login: Mapped[str] = mapped_column(String(25), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    update_at: Mapped[datetime] = mapped_column(DateTime,
                                                default=datetime.now(),
                                                onupdate=datetime.now())

    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="owner", cascade="all, delete-orphan")


class Task(Base):
    """
    Модель для таблицы задач.

    Атрибуты:
        id (int): Уникальный идентификатор задачи.
        is_done (bool): Статус выполнения задачи, по умолчанию False.
        name (str): Название задачи, максимум 50 символов.
        description (str): Описание задачи, максимум 250 символов.
        owner_id (int): Идентификатор владельца задачи.
        created_at (datetime): Дата и время создания задачи.
        update_at (datetime): Дата и время последнего обновления данных задачи.

    Связи:
        owner: Задача принадлежит одному пользователю.
    """
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(250))
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    update_at: Mapped[datetime] = mapped_column(DateTime,
                                                default=datetime.now(),
                                                onupdate=datetime.now())

    owner: Mapped["User"] = relationship("User", back_populates="tasks")


async def create_bd_tables() -> None:
    """
    Асинхронно создает все таблицы базы данных, определенные в моделях SQLAlchemy.

    Использует:
    - engine.begin(): Контекстный менеджер для начала асинхронной транзакции.
    - conn.run_sync(Base.metadata.create_all): Создает все таблицы базы данных, используя метаданные моделей.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
