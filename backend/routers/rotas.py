from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import BuscaHistorico
from services.routing import calcular_todas_rotas

router = APIRouter(prefix="/rotas", tags=["rotas"])


class RotaRequest(BaseModel):
    origem:     str
    destino:    str
    origem_lat: float
    origem_lng: float
    dest_lat:   float
    dest_lng:   float


@router.post("")
async def buscar_rotas(payload: RotaRequest, db: Session = Depends(get_db)):
    """
    Calcula rotas otimizadas entre origem e destino usando OSRM.
    Retorna tempo, custo e emissão de CO₂ para cada modal.
    """
    rotas = await calcular_todas_rotas(
        payload.origem_lat, payload.origem_lng,
        payload.dest_lat,   payload.dest_lng,
    )

    if not rotas:
        raise HTTPException(status_code=502, detail="Não foi possível calcular as rotas.")

    # Persiste a busca no histórico
    try:
        historico = BuscaHistorico(
            origem=payload.origem,   destino=payload.destino,
            origem_lat=payload.origem_lat, origem_lng=payload.origem_lng,
            dest_lat=payload.dest_lat,     dest_lng=payload.dest_lng,
        )
        db.add(historico)
        db.commit()
    except Exception:
        db.rollback()   # Não falha a requisição se o DB estiver indisponível

    return {"rotas": rotas}
