from enum import Enum
from sqlalchemy import Integer, Column, String, BigInteger

from spmi_vent_bot.database import Base

class Role(Enum):
    COMMON = 1
    OPERATOR = 2
    ADMIN = 3


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, unique=True)
    username = Column(String)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role_int = Column(Integer, default=1)
