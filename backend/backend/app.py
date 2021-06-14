from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.common.database import engine
from backend.common import models
from .endpoints import auth
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
app.include_router(auth.router)
