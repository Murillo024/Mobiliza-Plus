"""
Cálculo de emissão de CO₂ por modal de transporte.

Fontes:
- IPCC / Our World in Data (g CO₂ por passageiro-quilômetro)
- Dados adaptados ao contexto brasileiro
"""

# Fator de emissão em kg CO₂ por km percorrido (por passageiro)
FATORES_CO2: dict[str, float] = {
    "driving":   0.120,   # Carro particular médio
    "bus":       0.068,   # Ônibus urbano (média ocupação)
    "metro":     0.014,   # Metrô/trem (mix energético BR)
    "cycling":   0.000,   # Bicicleta
    "foot":      0.000,   # Caminhada
}


def calcular_co2(distancia_m: float, perfil: str) -> dict:
    """
    Retorna o CO₂ emitido para o percurso.

    Args:
        distancia_m: distância em metros retornada pelo OSRM
        perfil: 'driving' | 'cycling' | 'foot' | 'bus' | 'metro'

    Returns:
        dict com valor em kg, gramas e classificação
    """
    dist_km = distancia_m / 1000
    fator   = FATORES_CO2.get(perfil, 0.0)
    kg      = round(dist_km * fator, 3)

    if kg == 0:
        nivel = "zero"
    elif kg < 0.5:
        nivel = "baixo"
    elif kg < 2.0:
        nivel = "medio"
    else:
        nivel = "alto"

    return {
        "kg":    kg,
        "gramas": round(kg * 1000),
        "nivel": nivel,
        "label": f"{kg:.2f} kg CO₂",
    }


def comparar_co2(rotas: list[dict]) -> list[dict]:
    """
    Adiciona campo 'economia_co2' em relação à rota de carro mais poluente.
    """
    referencia = max((r["co2"]["kg"] for r in rotas), default=1) or 1
    for rota in rotas:
        economizado = referencia - rota["co2"]["kg"]
        rota["co2"]["economia_pct"] = round((economizado / referencia) * 100)
    return rotas
