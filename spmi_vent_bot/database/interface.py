from typing import overload, Sequence

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from spmi_vent_bot.database import User
from spmi_vent_bot.database.models import Role


class Database:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self,
                          user_id: int,
                          username: str,
                          first_name: str,
                          last_name: str,
                          role: Role = Role.COMMON):
        """
        Создание пользователя
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
            role_int=role.value,
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        await self.session.commit()

        return user

    @overload
    async def get_user(self, id: int) -> User | None:...
    @overload
    async def get_user(self, user_id: int) -> User | None:...
    @overload
    async def get_user(self, username: str) -> User | None:...

    async def get_user(self, **kwargs) -> User | None:
        """
        Получение пользователя по одному из параметров: id, user_id, username

        :param kwargs: id, user_id, username
        :return: User или None
        """
        stmt = ""
        if 'id' in kwargs:
            return await self.session.get(User, kwargs['id'])

        if 'user_id' in kwargs:
            stmt = select(User).where(User.user_id == kwargs['user_id'])

        if 'username' in kwargs:
            stmt = select(User).where(User.username == kwargs['username'])
        result = await self.session.execute(stmt)
        return result.scalars().first()

    @overload
    async def get_users(self, ids: list[int]) -> Sequence[User] | None:...

    @overload
    async def get_users(self, user_ids: list[int]) -> Sequence[User] | None:...

    @overload
    async def get_users(self, usernames: list[str]) -> Sequence[User] | None:...

    @overload
    async def get_users(self, role: Role) -> Sequence[User] | None:...

    async def get_users(self, **kwargs) -> Sequence[User] | None:
        """
        Получение списка пользователей по массиву параметров или же по роли
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

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_user(self,
                          user: User,
                          username: str = None,
                          first_name: str = None,
                          last_name: str = None,
                          role: Role = None) -> User | None:
        """
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
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_user(id=user.id)

    async def delete_user(self, user: User) -> None:
        stmt = delete(User).where(User.id == user.id)
        await self.session.execute(stmt)
        await self.session.commit()