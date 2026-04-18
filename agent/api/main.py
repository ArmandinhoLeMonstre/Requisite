from fastapi import FastAPI
from api.routers import agents_router
from api.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(agents_router.router, prefix="/api/agents", tags=["agents"])