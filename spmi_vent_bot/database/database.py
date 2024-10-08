from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from spmi_vent_bot.config import DB_URI
from spmi_vent_bot.database import Base

engine = create_async_engine(DB_URI)

session = sessionmaker(bind=engine, class_=AsyncSession)


def connect():
    """
    Подключение к базе данных
    :return:
    """
    engine.connect()


async def create():
    """
    Создание таблиц
    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
