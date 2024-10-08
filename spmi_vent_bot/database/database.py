from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from spmi_vent_bot.config import DB_URI
from spmi_vent_bot.database.models import User

engine = create_async_engine(DB_URI)

session = async_sessionmaker(bind=engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

    