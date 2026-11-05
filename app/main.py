from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.database import get_db, Game, Movimientos
from app.schemas import PartidaResponse, EstadisticasResponse, MovimientoRequest, MovimientosResponse
from typing import List
import app.logic as logic

app = FastAPI(title="API de Tic Tac Toe", version="1.0.0")

@app.get("/", response_class=HTMLResponse)
def interfaz_web():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Tres en Raya - Control por Teclado</title>
        <style>
            body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; background: #f4f4f9; padding: 20px; }
            h1 { color: #333; }
            .board { display: grid; grid-template-columns: repeat(3, 80px); grid-gap: 5px; margin: 20px 0; }
            .cell { width: 80px; height: 80px; font-size: 2rem; font-weight: bold; cursor: pointer; background: #fff; border: 2px solid #333; display: flex; align-items: center; justify-content: center; }
            .cell:disabled { cursor: not-allowed; background: #eee; }
            .info { font-size: 1.2rem; margin-bottom: 15px; }
            .guide { background: #e9ecef; padding: 10px 15px; border-radius: 5px; margin-top: 15px; text-align: center; font-size: 0.9rem; }
            button.new-game { padding: 10px 20px; font-size: 1rem; cursor: pointer; background: #007bff; color: white; border: none; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h1>Tres en Raya</h1>
        <button class="new-game" onclick="nuevaPartida()">Iniciar Nueva Partida (Tecla N)</button>
        
        <div class="info" id="estado-info">Haz clic en "Iniciar Nueva Partida" o pulsa N</div>
        
        <div class="board" id="tablero"></div>

        <div class="guide">
            <strong>Mapeo del Teclado Numérico:</strong><br>
            1 | 2 | 3 &nbsp;&nbsp;(Arriba)<br>
            4 | 5 | 6 &nbsp;&nbsp;(Centro)<br>
            7 | 8 | 9 &nbsp;&nbsp;(Abajo)
        </div>

        <script>
            let partidaId = null;
            let turnoActual = "X";
            let estadoJuego = "FINISHED";

            // Mapeo espacial: Teclado Numérico -> Casilla de la API (1 a 9)
            const MAPA_NUMPAD = {
                '1': 1, '2': 2, '3': 3,
                '4': 4, '5': 5, '6': 6,
                '7': 7, '8': 8, '9': 9
            };

            async function nuevaPartida() {
                const res = await fetch('/partidas', { method: 'POST' });
                const data = await res.json();
                partidaId = data.id;
                turnoActual = data.turno;
                estadoJuego = data.estado;
                actualizarPantalla(data);
            }

            async function hacerMovimiento(casilla) {
                if (estadoJuego !== "IN_PROGRESS") return;

                const res = await fetch(`/partidas/${partidaId}/movimientos`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ jugador: turnoActual, casilla: casilla })
                });

                if (!res.ok) {
                    const err = await res.json();
                    alert(err.detail);
                    return;
                }

                const data = await res.json();
                turnoActual = data.turno;
                estadoJuego = data.estado;
                actualizarPantalla(data);
            }

            function actualizarPantalla(data) {
                const info = document.getElementById('estado-info');
                if (data.estado === "IN_PROGRESS") {
                    info.textContent = `Partida #${data.id} | Turno de: [ ${data.turno} ]`;
                } else if (data.estado === "FINISHED") {
                    info.textContent = `¡Partida #${data.id} Finalizada! Ganador: ${data.ganador}`;
                } else {
                    info.textContent = `¡Partida #${data.id} en Empate!`;
                }

                const contenedor = document.getElementById('tablero');
                contenedor.innerHTML = '';
                
                for (let i = 0; i < 9; i++) {
                    const btn = document.createElement('button');
                    btn.className = 'cell';
                    const char = data.tablero[i];
                    btn.textContent = char === '*' ? '' : char;
                    btn.disabled = char !== '*' || data.estado !== "IN_PROGRESS";
                    btn.onclick = () => hacerMovimiento(i + 1);
                    contenedor.appendChild(btn);
                }
            }

            // Escuchador global de eventos de teclado
            document.addEventListener('keydown', (e) => {
                if (e.key.toLowerCase() === 'n') {
                    nuevaPartida();
                    return;
                }
                
                // Si la tecla presionada está en el mapa del numpad
                if (MAPA_NUMPAD[e.key]) {
                    hacerMovimiento(MAPA_NUMPAD[e.key]);
                }
            });
        </script>
    </body>
    </html>
    """
    
@app.post("/partidas", response_model=PartidaResponse, status_code=status.HTTP_201_CREATED)
def crear_partida(db: Session = Depends(get_db)):
    """
    Crea una nueva partida en la base de datos SQLite con el tablero inicial ("*********")
    y el turno asignado al Jugador 1 ("X").
    """
    nueva_partida = Game()
    db.add(nueva_partida)
    db.commit()
    db.refresh(nueva_partida)
    return nueva_partida


@app.get("/partidas/{id}", response_model=PartidaResponse, status_code=status.HTTP_200_OK)
def obtener_partida(id: int, db: Session = Depends(get_db)):
    """
    Obtiene la partida con el ID especificado desde la base de datos SQLite.
    Lanza un 404 Not Found si el ID no existe.
    """
    partida = db.query(Game).filter(Game.id == id).first()
    if not partida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Partida no encontrada"
        )
    return partida


@app.post("/partidas/{id}/movimientos", response_model=PartidaResponse, status_code=status.HTTP_200_OK)
def hacer_movimiento(id: int, movimiento: MovimientoRequest, db: Session = Depends(get_db)):
    """
    Registra un nuevo movimiento en la partida especificada.
    Valida la existencia de la partida, su estado, el turno y la casilla elegida
    antes de persistir los cambios en la base de datos.
    """
    # 1. Buscar la partida en SQLite
    partida = db.query(Game).filter(Game.id == id).first()
    if not partida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Partida no encontrada"
        )
        
    # 2. Verificar que la partida no haya concluido
    if partida.estado != "IN_PROGRESS":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La partida ya ha finalizado"
        )
    
    # 3. Aplicar el movimiento y validar reglas con app/logic.py
    tablero_lista = list(partida.tablero)
    try:
        nuevo_tablero_lista = logic.marcar_casilla(
            jugador=movimiento.jugador,
            casilla=movimiento.casilla,
            tablero=tablero_lista,
            jugador_actual=partida.turno
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
        
    # 4. Actualizar el tablero en formato string
    partida.tablero = "".join(nuevo_tablero_lista)
    
    nuevo_log = Movimientos(
        partida_id=partida.id,
        jugador=movimiento.jugador,
        casilla=movimiento.casilla
    )
    db.add(nuevo_log)
    # 5. Evaluar el estado del juego tras el movimiento
    if logic.verificar_ganador(nuevo_tablero_lista):
        partida.estado = "FINISHED"
        partida.ganador = movimiento.jugador
    elif logic.verificar_empate(nuevo_tablero_lista):
        partida.estado = "DRAW"
    else:
        # Pasar el turno al siguiente jugador
        partida.turno = "O" if movimiento.jugador == "X" else "X"

    # 6. Persistir cambios en SQLite y devolver la partida actualizada
    db.commit()
    db.refresh(partida)
    
    return partida


@app.get("/estadisticas", response_model=EstadisticasResponse, status_code=status.HTTP_200_OK)
def obtener_estadisticas(db: Session = Depends(get_db)):
    """
    Calcula y retorna estadísticas generales acumuladas en la base de datos SQLite:
    total de partidas, victorias del Jugador 1 ("X"), victorias del Jugador 2 ("O") y empates.
    """
    total = db.query(Game).count()
    victorias_1 = db.query(Game).filter(Game.ganador == "X").count()
    victorias_2 = db.query(Game).filter(Game.ganador == "O").count()
    empates = db.query(Game).filter(Game.estado == "DRAW").count()
    
    return {
        "total_partidas": total,
        "victorias_1": victorias_1,
        "victorias_2": victorias_2,
        "empates": empates
    }

@app.get("/partidas/{id}/logs", response_model=List[MovimientosResponse], status_code=status.HTTP_200_OK)
def obtener_logs_partida(id: int, db: Session = Depends(get_db)):
    """
    Retorna la lista cronológica de movimientos registrados para la partida especificada.
    """
    partida = db.query(Game).filter(Game.id == id).first()
    if not partida:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partida no encontrada")
    return partida.movimientos