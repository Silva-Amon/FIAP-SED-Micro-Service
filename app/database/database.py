from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./user.db"

engine = create_async_engine(
    DATABASE_URL, echo=True,
    connect_args={"check_same_thread": False}
)

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
    )


Base = declarative_base()
