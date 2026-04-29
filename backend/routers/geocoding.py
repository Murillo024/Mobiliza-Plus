from fastapi import APIRouter, Query
from services.geocoding import buscar_sugestoes

router = APIRouter(prefix="/geocoding", tags=["geocoding"])


@router.get("/sugestoes")
async def sugestoes(q: str = Query(..., min_length=3)):
    """
    Retorna sugestões de endereços via Nominatim (OpenStreetMap).
    Usar como autocomplete no frontend.
    """
    return await buscar_sugestoes(q)
