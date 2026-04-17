from fastapi import FastAPI
from api.routers.agents_router import router as agent_router
from api.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(agent_router)