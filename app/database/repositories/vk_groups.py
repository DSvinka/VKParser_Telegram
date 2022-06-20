from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.vk_group import VKGroup, VKGroupAdd, VKGroupUpdate


class VKGroupsRepository(object):
    def __init__(self, session):
        self.session = session

    async def get_all(self) -> list[VKGroup]:
        query = select(VKGroup)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, model_id: int) -> Optional[VKGroup]:
        query = select(VKGroup).where(VKGroup.id == model_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_vk_id(self, vk_id: str) -> Optional[VKGroup]:
        query = select(VKGroup).where(VKGroup.vk_id == vk_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    def add(self, model_add: VKGroupAdd) -> VKGroup:
        model = VKGroup.from_orm(model_add)

        self.session.add(model)
        return model

    def update(self, model: VKGroup, model_update: VKGroupUpdate) -> VKGroup:
        for var, value in vars(model_update).items():
            if not hasattr(model, var):
                continue
            setattr(model, var, value) if value else None

        self.session.add(model)
        return model

    async def delete(self, model: VKGroup) -> None:
        await self.session.delete(model)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, model: VKGroup):
        await self.session.refresh(model)

