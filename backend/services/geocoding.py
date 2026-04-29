"""
Geocodificação via Nominatim (OpenStreetMap) — gratuito, sem chave de API.
Regras de uso: https://operations.osmfoundation.org/policies/nominatim/
  - Máximo 1 requisição por segundo
  - Obrigatório informar User-Agent identificando a aplicação
"""

import httpx

NOMINATIM_URL = "https://nominatim.openstreetmap.org"
HEADERS = {
    "User-Agent": "Mobiliza+ - Projeto Acadêmico Facens",
    "Accept-Language": "pt-BR,pt;q=0.9",
}


async def buscar_sugestoes(query: str, limite: int = 5) -> list[dict]:
    """
    Retorna sugestões de endereços para autocomplete.
    Filtra por Brasil (countrycodes=br).
    """
    if not query or len(query) < 3:
        return []

    params = {
        "q":            query,
        "format":       "json",
        "limit":        limite,
        "countrycodes": "br",
        "addressdetails": 1,
    }

    try:
        async with httpx.AsyncClient(timeout=8) as client:
            resp = await client.get(f"{NOMINATIM_URL}/search", params=params, headers=HEADERS)
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return []

    return [
        {
            "place_id":    item["place_id"],
            "display_name": item["display_name"],
            "lat":          float(item["lat"]),
            "lon":          float(item["lon"]),
            "tipo":         item.get("type", ""),
        }
        for item in data
    ]


async def geocodificar(query: str) -> dict | None:
    """
    Retorna as coordenadas (lat/lon) do primeiro resultado para um endereço.
    """
    results = await buscar_sugestoes(query, limite=1)
    return results[0] if results else None
