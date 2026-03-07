from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers.shop_router import router as shop_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # db_conn_test()

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(shop_router)