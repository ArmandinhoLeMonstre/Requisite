from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config import settings


db_url = settings.database_url
engine = create_async_engine(db_url, echo=False)


AsyncSessionLocal = async_sessionmaker(
	engine,
	class_=AsyncSession,
	expire_on_commit=False, #Video Corey Schafer
)


class Base(DeclarativeBase):
	pass


async def get_db():
	async with AsyncSessionLocal() as db:
		yield db