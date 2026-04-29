from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime, timezone
from database import Base


class BuscaHistorico(Base):
    """Salva o histórico de buscas dos usuários."""
    __tablename__ = "buscas_historico"

    id         = Column(Integer, primary_key=True, index=True)
    origem     = Column(String(255), nullable=False)
    destino    = Column(String(255), nullable=False)
    origem_lat = Column(Float)
    origem_lng = Column(Float)
    dest_lat   = Column(Float)
    dest_lng   = Column(Float)
    criado_em  = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class RotaCache(Base):
    """Cache de rotas já calculadas para reduzir chamadas ao OSRM."""
    __tablename__ = "rotas_cache"

    id         = Column(Integer, primary_key=True, index=True)
    origem_lat = Column(Float, nullable=False)
    origem_lng = Column(Float, nullable=False)
    dest_lat   = Column(Float, nullable=False)
    dest_lng   = Column(Float, nullable=False)
    perfil     = Column(String(20), nullable=False)   # driving | cycling | foot
    dados      = Column(JSON, nullable=False)          # resposta completa do OSRM
    criado_em  = Column(DateTime, default=lambda: datetime.now(timezone.utc))
