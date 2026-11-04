import sqlalchemy as db
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Column, Integer, String, Char
from sqlalchemy.ext.declarative import declarative_base

engine = db.create_engine("sqlite:///game.db", connect_args={"check_same_thread": False})

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Game(Base):
    __tablename__ = 'tic_tac_toe'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tablero = Column(String, default="*********")  # Representación del tablero como una cadena de 9 caracteres
    turno = Column(String(1), default="X")  # Turno actual, puede ser 'X' o 'O'
    estado = Column(String, default="EN_PROGRESO")  
    ganador = Column(String(1), nullable=True)


Base.metadata.create_all(bind=engine)