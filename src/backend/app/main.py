import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import init_db
from app.routers import documents, chat, notifications
from app.routers.interactions import router as interactions_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("youvisa.main")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    logger.info("SQLite database initialised")
    yield


app = FastAPI(
    title="YOUVISA Platform",
    description="Plataforma Inteligente de Acompanhamento de Processos Consulares — Sprint 4",
    version="4.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router,      prefix="/api/documents",     tags=["documents"])
app.include_router(chat.router,           prefix="/api/chat",          tags=["chat"])
app.include_router(notifications.router,  prefix="/api/notifications", tags=["notifications"])
app.include_router(interactions_router,   prefix="/api/interactions",  tags=["interactions"])


@app.get("/")
async def root():
    return {
        "message": "YOUVISA Sprint 4 — Plataforma Multiagente de Processos Consulares",
        "version": "4.0.0",
        "endpoints": [
            "/api/documents",
            "/api/chat",
            "/api/notifications",
            "/api/interactions",
            "/docs",
        ],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
