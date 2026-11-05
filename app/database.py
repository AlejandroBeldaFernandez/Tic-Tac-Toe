import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
# Conexión a SQLite local. 
# check_same_thread=False permite la interacción multihilo requerida por FastAPI.
engine = db.create_engine("sqlite:///game.db", connect_args={"check_same_thread": False})

# Base declarativa para la definición del modelo ORM
Base = declarative_base()

# Fábrica de sesiones explícitas (sin autocommit ni autoflush automático)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Movimientos(Base):
    """
    Modelo ORM para mapear la tabla 'movimientos' en la base de datos SQLite.
    """
    __tablename__ = 'movimientos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    partida_id = Column(Integer, ForeignKey("tic_tac_toe.id"), nullable=False)
    jugador = Column(String(1), nullable=False)
    casilla = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    partida = relationship("Game", back_populates="movimientos")

class Game(Base):
    """
    Modelo ORM para mapear la tabla 'tic_tac_toe' en la base de datos SQLite.
    """
    __tablename__ = 'tic_tac_toe'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tablero = Column(String, default="*********")
    turno = Column(String(1), default="X")
    estado = Column(String, default="IN_PROGRESS")
    ganador = Column(String(1), nullable=True)
    
    movimientos = relationship("Movimientos", back_populates="partida", cascade="all, delete-orphan")


def get_db():
    """
    Inyección de dependencia para FastAPI.
    Provee una sesión limpia por cada petición HTTP y garantiza su cierre al finalizar.
    """
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close() 

# Creación automática del esquema en la base de datos si no existe
Base.metadata.create_all(bind=engine)