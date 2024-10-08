from enum import Enum
from sqlalchemy import Integer, Column, String, Boolean, BigInteger

from spmi_vent_bot.database.database import Base

class Role(Enum):
    COMMON = "COMMON"
    OPERATOR = "OPERATOR"
    ADMIN = "ADMIN"  


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, unique=True)
    username = Column(String)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role_int = Column(Integer, default=1)

    def __post_init__(self):
        self.role = Role(self.role_int)
