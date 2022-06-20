from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.chat import Chat, ChatAdd, ChatUpdate


class ChatsRepository(object):
    def __init__(self, session):
        self.session = session

    async def get_all(self) -> list[Chat]:
        query = select(Chat)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, model_id: int) -> Optional[Chat]:
        query = select(Chat).where(Chat.id == model_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_chat_id(self, chat_id: str) -> Optional[Chat]:
        query = select(Chat).where(Chat.chat_id == chat_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    def add(self, model_add: ChatAdd) -> Chat:
        model = Chat.from_orm(model_add)

        self.session.add(model)
        return model

    def update(self, model: Chat, model_update: ChatUpdate) -> Chat:
        for var, value in vars(model_update).items():
            if not hasattr(model, var):
                continue
            setattr(model, var, value) if value else None

        self.session.add(model)
        return model

    async def delete(self, model: Chat) -> None:
        await self.session.delete(model)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, model: Chat):
        await self.session.refresh(model)
