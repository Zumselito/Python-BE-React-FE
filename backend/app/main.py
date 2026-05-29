from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.client import ensure_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_table()
    yield


app = FastAPI(
    title="NutriTrack API",
    description="Zutaten-Datenbank mit vollständigen Nährwertdaten",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

# AWS Lambda handler
handler = Mangum(app)
