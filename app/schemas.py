from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal

class MovimientoRequest(BaseModel):
    jugador: Literal["X", "O"]
    casilla: int = Field(..., ge=0, le=8)
    
class PartidaResponse(BaseModel):
    id: int
    tablero: str
    turno: str
    estado: str
    ganador: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    
class EstadisticasResponse(BaseModel):
    total_partidas: int
    victorias_1: int
    victorias_2: int
    empates: int