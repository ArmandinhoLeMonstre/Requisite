from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings


sqlite_url = settings.database_url
engine = create_engine(sqlite_url, echo=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
	pass


#FastApi dependecy injection calls this function for each request and handles the clean up automaticaly
def get_db():  #dependency function that provides sessions to our routes, its a generator using the Yiel db, and using "with SessionsLocal()" it ensures a clean up even if an error occurs, it makes the session work as a context manager (kinda like opening a file)
	with SessionLocal() as db:
		yield db