from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.access_token import AccessToken, AccessTokenAdd, AccessTokenUpdate
from secrets import compare_digest


class AccessTokensRepository(object):
    def __init__(self, session):
        self.session = session

    async def get_all(self) -> list[AccessToken]:
        query = select(AccessToken)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, model_id: int) -> Optional[AccessToken]:
        query = select(AccessToken).where(AccessToken.id == model_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_chat_id(self, chat_id: str) -> Optional[AccessToken]:
        query = select(AccessToken).where(AccessToken.chat_id == chat_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_token(self, token: str) -> Optional[AccessToken]:
        query = select(AccessToken).where(AccessToken.token == token)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    def add(self, model_add: AccessTokenAdd) -> AccessToken:
        model = AccessToken.from_orm(model_add)

        self.session.add(model)
        return model

    def update(self, model: AccessToken, model_update: AccessTokenUpdate) -> AccessToken:
        for var, value in vars(model_update).items():
            if not hasattr(model, var):
                continue
            setattr(model, var, value) if value else None

        self.session.add(model)
        return model

    async def delete(self, model: AccessToken) -> None:
        await self.session.delete(model)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, model: AccessToken):
        await self.session.refresh(model)

