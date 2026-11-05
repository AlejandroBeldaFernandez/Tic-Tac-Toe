import pytest
from fastapi.testclient import TestClient
from app.main import app

# Cliente de pruebas para realizar peticiones HTTP simuladas a FastAPI
client = TestClient(app)


def test_crear_partida():
    """
    Verifica que POST /partidas cree una partida con estado IN_PROGRESS,
    el tablero inicial ("*********") y el turno para la ficha 'X'.
    """
    response = client.post("/partidas")
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["tablero"] == "*********"
    assert data["turno"] == "X"
    assert data["estado"] == "IN_PROGRESS"
    assert data["ganador"] is None


def test_obtener_partida_existente():
    """
    Verifica que GET /partidas/{id} retorne los datos de una partida válida.
    """
    res_crear = client.post("/partidas")
    partida_id = res_crear.json()["id"]

    response = client.get(f"/partidas/{partida_id}")
    assert response.status_code == 200
    assert response.json()["id"] == partida_id


def test_obtener_partida_inexistente():
    """
    Verifica que GET /partidas/{id} devuelva un error 404 Not Found si el ID no existe.
    """
    response = client.get("/partidas/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Partida no encontrada"


def test_movimiento_valido():
    """
    Verifica que un movimiento legal (Jugador X en la casilla 1) actualice el tablero y el turno a 'O'.
    """
    res_crear = client.post("/partidas")
    partida_id = res_crear.json()["id"]

    response = client.post(
        f"/partidas/{partida_id}/movimientos",
        json={"jugador": "X", "casilla": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tablero"] == "X********"
    assert data["turno"] == "O"


def test_movimiento_fuera_de_turno():
    """
    Verifica que si le toca a 'X' y mueve 'O', la API rechace la jugada con HTTP 400.
    """
    res_crear = client.post("/partidas")
    partida_id = res_crear.json()["id"]

    response = client.post(
        f"/partidas/{partida_id}/movimientos",
        json={"jugador": "O", "casilla": 1}
    )
    assert response.status_code == 400


def test_movimiento_casilla_ocupada():
    """
    Verifica que no se pueda marcar una casilla en la que ya hay una ficha.
    """
    res_crear = client.post("/partidas")
    partida_id = res_crear.json()["id"]

    # Jugador X marca la casilla central (5)
    client.post(f"/partidas/{partida_id}/movimientos", json={"jugador": "X", "casilla": 5})

    # Jugador O intenta marcar la misma casilla central (5)
    response = client.post(f"/partidas/{partida_id}/movimientos", json={"jugador": "O", "casilla": 5})
    assert response.status_code == 400


def test_movimiento_casilla_invalida_pydantic():
    """
    Verifica que si se envía una casilla fuera del rango 1-9 (ej. 0 o 10),
    Pydantic devuelva un error HTTP 422 Unprocessable Entity.
    """
    res_crear = client.post("/partidas")
    partida_id = res_crear.json()["id"]

    response = client.post(
        f"/partidas/{partida_id}/movimientos",
        json={"jugador": "X", "casilla": 10}
    )
    assert response.status_code == 422


def test_flujo_victoria_jugador_1():
    """
    Simula una partida completa donde el Jugador 1 ('X') gana completando la primera fila (casillas 1, 2, 3).
    """
    res_crear = client.post("/partidas")
    partida_id = res_crear.json()["id"]

    # Secuencia de jugadas:
    # X: 1, O: 4, X: 2, O: 5, X: 3 -> Fila superior completa
    client.post(f"/partidas/{partida_id}/movimientos", json={"jugador": "X", "casilla": 1})
    client.post(f"/partidas/{partida_id}/movimientos", json={"jugador": "O", "casilla": 4})
    client.post(f"/partidas/{partida_id}/movimientos", json={"jugador": "X", "casilla": 2})
    client.post(f"/partidas/{partida_id}/movimientos", json={"jugador": "O", "casilla": 5})
    
    res_final = client.post(f"/partidas/{partida_id}/movimientos", json={"jugador": "X", "casilla": 3})
    data = res_final.json()

    assert data["estado"] == "FINISHED"
    assert data["ganador"] == "X"


def test_estadisticas():
    """
    Verifica que el endpoint GET /estadisticas retorne la estructura con los conteos globales.
    """
    response = client.get("/estadisticas")
    assert response.status_code == 200
    data = response.json()
    assert "total_partidas" in data
    assert "victorias_1" in data
    assert "victorias_2" in data
    assert "empates" in data
    
def test_log_movimientos():
    """
    Verifica que cada movimiento realizado se registre en el historial de la partida (GET /partidas/{id}/logs).
    """
    # 1. Crear nueva partida
    res_crear = client.post("/partidas")
    partida_id = res_crear.json()["id"]

    # 2. Realizar dos movimientos válidos
    client.post(f"/partidas/{partida_id}/movimientos", json={"jugador": "X", "casilla": 5})
    client.post(f"/partidas/{partida_id}/movimientos", json={"jugador": "O", "casilla": 1})

    # 3. Consultar los logs de la partida
    response = client.get(f"/partidas/{partida_id}/logs")
    assert response.status_code == 200
    logs = response.json()

    # 4. Validar que se hayan registrado exactamente 2 movimientos en orden
    assert len(logs) == 2
    assert logs[0]["jugador"] == "X" and logs[0]["casilla"] == 5
    assert logs[1]["jugador"] == "O" and logs[1]["casilla"] == 1