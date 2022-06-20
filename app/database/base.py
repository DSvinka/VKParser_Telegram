import os
from contextlib import contextmanager

from app.config import config
from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    config['database']['url'],
    echo=bool(config['database']['echo']),
    future=True
)

get_async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
