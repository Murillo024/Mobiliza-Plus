"""
Integração com OSRM (Open Source Routing Machine).
API pública gratuita — sem necessidade de chave de API.
Documentação: https://project-osrm.org/docs/v5.5.1/api/
"""

import httpx
from services.co2 import calcular_co2

OSRM_BASE = "https://router.project-osrm.org/route/v1"

# Perfis disponíveis no OSRM público
PERFIS_OSRM = {
    "driving": "driving",
    "cycling": "cycling",
    "foot":    "foot",
}

# Mapeamento perfil → nome amigável e ícone
INFO_PERFIL = {
    "driving": {"label": "Mais Rápida",  "icone": "🚌", "cor": "#1bc98e", "tipo": "rapida"},
    "cycling": {"label": "Sustentável",  "icone": "🚲", "cor": "#22c55e", "tipo": "eco"},
    "foot":    {"label": "Mais Barata",  "icone": "🚶", "cor": "#f59e0b", "tipo": "barata"},
}


async def calcular_rota(
    orig_lat: float, orig_lng: float,
    dest_lat: float, dest_lng: float,
    perfil: str = "driving"
) -> dict | None:
    """
    Consulta o OSRM e retorna rota enriquecida com CO₂.
    Retorna None se a API não responder ou não encontrar rota.
    """
    profile_key = PERFIS_OSRM.get(perfil, "driving")
    url = (
        f"{OSRM_BASE}/{profile_key}/"
        f"{orig_lng},{orig_lat};{dest_lng},{dest_lat}"
        "?overview=full&geometries=geojson&steps=false"
    )

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return None

    if data.get("code") != "Ok" or not data.get("routes"):
        return None

    route = data["routes"][0]
    dist_m  = route["distance"]
    dur_s   = route["duration"]
    mins    = max(1, round(dur_s / 60))
    dist_km = dist_m / 1000

    info = INFO_PERFIL[perfil]
    co2  = calcular_co2(dist_m, perfil)

    # Custo estimado (simplificado para demonstração)
    custo = _estimar_custo(perfil, dist_km)

    return {
        "perfil":    perfil,
        "tipo":      info["tipo"],
        "label":     info["label"],
        "icone":     info["icone"],
        "cor":       info["cor"],
        "tempo":     f"{mins} min",
        "custo":     custo,
        "distancia": f"{dist_km:.1f} km",
        "co2":       co2,
        "geometry":  route["geometry"],   # GeoJSON LineString
    }


async def calcular_todas_rotas(
    orig_lat: float, orig_lng: float,
    dest_lat: float, dest_lng: float,
) -> list[dict]:
    """Calcula rotas para driving, cycling e foot em paralelo."""
    import asyncio

    tasks = [
        calcular_rota(orig_lat, orig_lng, dest_lat, dest_lng, p)
        for p in ["driving", "cycling", "foot"]
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    rotas = [r for r in results if isinstance(r, dict)]

    # Ordena: rapida → barata → eco
    ordem = {"rapida": 0, "barata": 1, "eco": 2}
    rotas.sort(key=lambda r: ordem.get(r["tipo"], 9))

    # Marca a mais rápida como recomendada
    if rotas:
        rotas[0]["destaque"] = True

    return rotas


def _estimar_custo(perfil: str, dist_km: float) -> str:
    """Estimativa simples de custo em BRL."""
    if perfil == "driving":
        # Tarifa de transporte público SP ~R$4,40
        return "R$ 4,40"
    if perfil == "foot":
        return "R$ 0,00"
    if perfil == "cycling":
        return "R$ 0,00"
    return "R$ 0,00"
