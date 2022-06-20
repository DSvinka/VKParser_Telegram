from typing import Optional

from sqlmodel import SQLModel, Field


class AccessTokenBase(SQLModel):
    __tablename__ = 'access_tokens'

    chat_id: Optional[str] = Field(default=None, nullable=True)
    token: str = Field(default="ERROR_NoToken", nullable=False)


class AccessToken(AccessTokenBase, table=True):
    id: int = Field(default=None, primary_key=True)


class AccessTokenAdd(AccessTokenBase):
    pass


class AccessTokenUpdate(SQLModel):
    chat_id: Optional[str] = None
    token: Optional[str] = None
