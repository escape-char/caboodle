from fastapi import FastAPI
from backend.common.database import engine
from backend.common import models
from .endpoints import auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
