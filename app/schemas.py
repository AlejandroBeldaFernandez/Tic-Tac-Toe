from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class MovimientoRequest(BaseModel):
    """
    Esquema de validación de entrada para peticiones de jugada.
    - jugador: Restringido estrictamente a "X" u "O".
    - casilla: Restringido a un entero entre 0 y 8.
    """
    jugador: Literal["X", "O"]
    casilla: int = Field(...,ge=1, le=9, description="Número de casilla entre 1 y 9 (inclusive)")

class PartidaResponse(BaseModel):
    """
    Esquema de salida para el estado de una partida.
    Configurado con from_attributes=True para mapear directamente desde modelos de SQLAlchemy.
    """
    id: int
    tablero: str
    turno: str
    estado: str
    ganador: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class MovimientosResponse(BaseModel):
    
    id: int
    partida_id: int
    jugador: str
    casilla: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
    
class EstadisticasResponse(BaseModel):
    """
    Esquema de salida para la consulta del marcador e historial general.
    """
    total_partidas: int
    victorias_1: int
    victorias_2: int
    empates: int