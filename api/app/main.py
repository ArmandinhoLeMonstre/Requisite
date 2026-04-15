from fastapi import FastAPI
from contextlib import asynccontextmanager


app = FastAPI()

@app.get("/")
def root():
    return {"Petit", "Zeub"}