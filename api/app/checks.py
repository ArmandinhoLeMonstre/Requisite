from app.database import AsyncSessionLocal
from sqlalchemy import text
from app.logger import logger

async def check_db():
	try:
		async with AsyncSessionLocal() as db:
			await db.execute(text("SELECT 1"))
			logger.info("database.start.check", message="Database startup check ok")
	except Exception as e:
		logger.error("database.start.check.error", exc_info=True, step="check_db")
		raise