from typing import overload, Sequence

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from spmi_vent_bot.database.models.user import Role, User

@overload
async def get_user(session: AsyncSession, id: int) -> User | None: ...
@overload
async def get_user(session: AsyncSession, user_id: int) -> User | None: ...
@overload
async def get_user(session: AsyncSession, username: str) -> User | None: ...


async def get_user(session: AsyncSession, **kwargs) -> User | None:
    """
    Получение пользователя по одному из параметров: id, user_id, username
    :param session: AsyncSession
    :param kwargs: id, user_id, username
    :return: User или None
    """
    stmt = ""
    if 'id' in kwargs:
        stmt = select(User).where(User.id == kwargs['id'])
    
    if 'user_id' in kwargs:
        stmt = select(User).where(User.user_id == kwargs['user_id'])
    
    if 'username' in kwargs:
        stmt = select(User).where(User.username == kwargs['username'])
    result = await session.execute(stmt)
    return result.scalars().first()

@overload
async def get_users(session: AsyncSession, ids: list[int]) -> Sequence[User] | None: ...
@overload
async def get_users(session: AsyncSession, user_ids: list[int]) -> Sequence[User] | None: ...
@overload
async def get_users(session: AsyncSession, usernames: list[str]) -> Sequence[User] | None: ...
@overload
async def get_users(session: AsyncSession, role: Role) -> Sequence[User] | None: ...


async def get_users(session: AsyncSession, **kwargs) -> Sequence[User] | None:
    """
    Получение списка пользователей по массиву параметров или же по роли
    :param session: AsyncSession
    :param kwargs: ids, user_ids, usernames, role
    :return: Sequence[User] | None
    """
    stmt = ""
    if 'ids' in kwargs:
        stmt = select(User).where(User.id.in_(kwargs['ids']))
    
    if 'user_ids' in kwargs:
        stmt = select(User).where(User.user_id.in_(kwargs['user_ids']))
    
    if 'usernames' in kwargs:
        stmt = select(User).where(User.username.in_(kwargs['usernames']))
    
    if 'role' in kwargs: 
        stmt = select(User).where(User.role_int == kwargs['role'].value)

    result = await session.execute(stmt)
    return result.scalars().all()


def create_user(session: AsyncSession,
                user_id: int,
                username: str,
                first_name: str,
                last_name: str,
                role: Role = Role.COMMON):
    """
    Создание пользователя
    :param session: AsyncSession
    :param user_id: user_id телеграмма
    :param username: username телеграмма
    :param first_name: имя
    :param last_name: фамилия
    :param role: роль пользователя
    :return:
    """
    user = User(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        _role_int=role.value,
    )
    session.add(user)
    session.commit()
    return user
    
    
async def update_user(session: AsyncSession,
                user: User,
                username: str = None,
                first_name: str = None,
                last_name: str = None,
                role: Role = None) -> User | None:
    """

    :param session: AsyncSession
    :param user: User - объект пользователя
    :param username: username телеграмма
    :param first_name: имя
    :param last_name: фамилия
    :param role: роль
    :return:
    """
    stmt = update(User).where(User.id == user.id).values(
        username=username if username else user.username,
        first_name=first_name if first_name else user.first_name,
        last_name=last_name if last_name else user.last_name,
        role_int=role.value if role else user.role_int
    )
    await session.execute(stmt)
    return await get_user(session, id=user.id)


async def delete_user(session: AsyncSession, user: User):
    stmt = delete(User).where(User.id == user.id)
    await session.execute(stmt)