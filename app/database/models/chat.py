from typing import Optional

from sqlmodel import SQLModel, Field


class ChatBase(SQLModel):
    __tablename__ = 'chats'

    chat_id: str = Field(default="ERROR_NoChatId", nullable=False)


class Chat(ChatBase, table=True):
    id: int = Field(default=None, primary_key=True)


class ChatAdd(ChatBase):
    pass


class ChatUpdate(SQLModel):
    chat_id: Optional[str] = None
