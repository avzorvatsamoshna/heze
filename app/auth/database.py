from datetime import datetime
from typing import AsyncGenerator
from sqlalchemy import Column, String, Integer, create_engine, Boolean
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost/baza"
Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String(length=1024), nullable=False)
    is_admin = Column(Boolean)
    is_developer = Column(Boolean)
    is_user = Column(Boolean)
engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
