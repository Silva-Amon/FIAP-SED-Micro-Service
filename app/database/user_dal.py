from typing import List

from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.user import User
import uuid
from datetime import datetime


class UserDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, new_user: User):
        new_user.id = str(uuid.uuid4())
        new_user.active = True
        new_user.createdAt = datetime.now()

        self.db_session.add(new_user)
        await self.db_session.flush()

    async def get_all(self) -> List[User]:
        q = await self.db_session.execute(select(User).order_by(User.id))
        return q.scalars().all()

    async def get(self, user_id: str) -> User | None:
        q = await self.db_session.execute(select(User).where(User.id == user_id))
        return q.scalars().first()

    async def get_by_email(self, email: str) -> User | None:
        q = await self.db_session.execute(select(User).where(User.email == email))
        return q.scalars().first()

    async def update(self, user_updated: User):
        q = update(User).where(User.id == user_updated.id)
        q = q.values(name=user_updated.name, username=user_updated.username,
                     email=user_updated.email)

        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)

    async def delete(self, user_id: str):
        q = delete(User).where(User.id == user_id)
        await self.db_session.execute(q)
