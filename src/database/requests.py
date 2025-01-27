from sqlalchemy import select, delete

from src.database.conn import async_session
from src.database.models import User, Task


async def add_user(user_data: dict) -> None:
    """
    Добавляет нового пользователя в базу данных.

    Аргументы:
        user_data (dict): Словарь с данными пользователя. Должен содержать ключи 'tg_id', 'name' и 'login'.
    """
    async with async_session() as session:
        session.add(User(
            tg_id=user_data['tg_id'],
            name=user_data['name'],
            login=user_data['login']
        ))
        await session.commit()


async def get_user_id_by_tg_id(tg_id: int) -> int:
    """
    Получает идентификатор пользователя по его идентификатору в Telegram.

    Аргументы:
        tg_id (int): Идентификатор пользователя в Telegram.

    Возвращает:
        int: Идентификатор пользователя в базе данных.
    """
    async with async_session() as session:
        return await session.scalar(select(User.id).where(User.tg_id == tg_id))


async def add_task(task_data: dict) -> None:
    """
    Добавляет новую задачу в базу данных.

    Аргументы:
        task_data (dict): Словарь с данными задачи. Должен содержать ключи 'name', 'description' и 'owner_id'.
    """
    async with async_session() as session:
        session.add(Task(
            name=task_data['name'],
            description=task_data['description'],
            owner_id=task_data['owner_id']
        ))
        await session.commit()


async def get_all_tasks_list(tg_id: int) -> list[Task]:
    """
    Получает список всех задач пользователя по его идентификатору в Telegram.

    Аргументы:
        tg_id (int): Идентификатор пользователя в Telegram.

    Возвращает:
        list[Task]: Список всех задач пользователя, отсортированных по полю 'is_done'.
    """
    async with async_session() as session:
        user_subquery = select(User.id).where(User.tg_id == tg_id).scalar_subquery()
        result = await session.scalars(
            select(Task).where(Task.owner_id == user_subquery).order_by(Task.is_done)
        )
        return result


async def get_completed_tasks_list(tg_id: int) -> list[Task]:
    """
    Получает список завершенных задач пользователя по его идентификатору в Telegram.

    Аргументы:
        tg_id (int): Идентификатор пользователя в Telegram.

    Возвращает:
        list[Task]: Список завершенных задач пользователя.
    """
    async with async_session() as session:
        user_subquery = select(User.id).where(User.tg_id == tg_id).scalar_subquery()
        result = await session.scalars(
            select(Task).where(Task.owner_id == user_subquery, Task.is_done == True)
        )
        return result


async def get_actual_tasks_list(tg_id: int) -> list[Task]:
    """
    Получает список актуальных (незавершенных) задач пользователя по его идентификатору в Telegram.

    Аргументы:
        tg_id (int): Идентификатор пользователя в Telegram.

    Возвращает:
        list[Task]: Список актуальных задач пользователя.
    """
    async with async_session() as session:
        user_subquery = select(User.id).where(User.tg_id == tg_id).scalar_subquery()
        result = await session.scalars(
            select(Task).where(Task.owner_id == user_subquery, Task.is_done == False)
        )
        return result


async def get_task_by_id(task_id: int) -> Task:
    """
    Получает задачу по её идентификатору.

    Аргументы:
        task_id (int): Идентификатор задачи.

    Возвращает:
        Task: Объект задачи.
    """
    async with async_session() as session:
        return await session.scalar(select(Task).where(Task.id == task_id))


async def mark_task_as_complete(task_id: int) -> None:
    """
    Помечает задачу как выполненную.

    Аргументы:
        task_id (int): Идентификатор задачи.
    """
    async with async_session() as session:
        async with session.begin():
            task = await session.scalar(select(Task).where(Task.id == task_id))
            if task:
                task.is_done = True
                await session.commit()


async def delete_task(task_id: int) -> None:
    """
    Удаляет задачу по её идентификатору.

    Аргументы:
        task_id (int): Идентификатор задачи.
    """
    async with async_session() as session:
        async with session.begin():
            task = await session.scalar(select(Task).where(Task.id == task_id))
            if task:
                await session.delete(task)
                await session.commit()


async def delete_completed_tasks(tg_id: int) -> None:
    """
    Удаляет все завершенные задачи пользователя по его идентификатору в Telegram.

    Аргументы:
        tg_id (int): Идентификатор пользователя в Telegram.
    """
    async with async_session() as session:
        async with session.begin():
            completed_tasks = await get_completed_tasks_list(tg_id)
            completed_tasks_id = [task.id for task in completed_tasks]

            print(completed_tasks_id)
            await session.execute(
                delete(Task).where(Task.id.in_(completed_tasks_id))
            )
            await session.commit()
