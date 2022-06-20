from typing import Optional

from sqlmodel import SQLModel, Field


class VKGroupBase(SQLModel):
    __tablename__ = 'vk_groups'

    vk_id: str = Field(default="ERROR_NoVkId", nullable=False)
    name: str = Field(default="ERROR_NoName", nullable=False)
    url: str = Field(default="ERROR_NoUrl", nullable=False)

    last_post_id: Optional[int] = Field(nullable=True)


class VKGroup(VKGroupBase, table=True):
    id: int = Field(default=None, primary_key=True)


class VKGroupAdd(VKGroupBase):
    pass


class VKGroupUpdate(SQLModel):
    vk_id: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None

    last_post_id: Optional[int] = None
