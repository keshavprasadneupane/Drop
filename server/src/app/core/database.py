from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends
from typing import AsyncGenerator, Annotated
from app.models.base import Base
from  app.settings import settings


engine = create_async_engine( settings.DATABASE_URL , echo = True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)



async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
      await db.close()


DB = Annotated[AsyncSession, Depends(get_db)]