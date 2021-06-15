from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.common.database import engine
from backend.common import models
from .endpoints import routers
from .settings import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

for r in routers:
    app.include_router(r)
