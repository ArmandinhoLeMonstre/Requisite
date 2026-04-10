from fastapi import FastAPI
from api.routers.agents_router import router as agent_router

app = FastAPI()

app.include_router(agent_router)