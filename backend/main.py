from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import create_tables
from routers import rotas, geocoding


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Cria as tabelas no MySQL ao iniciar."""
    try:
        create_tables()
    except Exception as e:
        # Continua mesmo se o banco não estiver disponível (ex: dev sem MySQL)
        print(f"[AVISO] Não foi possível criar tabelas: {e}")
    yield


app = FastAPI(
    title="Mobiliza+ API",
    description="API de mobilidade urbana com rotas multimodais e cálculo de CO₂",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGIN, "http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rotas.router,     prefix="/api")
app.include_router(geocoding.router, prefix="/api")


@app.get("/")
def healthcheck():
    return {"status": "ok", "app": "Mobiliza+"}
