from typing import AsyncGenerator

from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = None # URL to database

engine: AsyncEngine = create_async_engine(DATABASE_URL)

session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:    
    yield session_maker()