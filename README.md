# Tres en Raya Backend API 

Backend para el juego del Tres en Raya desarrollado en Python utilizando **FastAPI**, **SQLite**, **SQLAlchemy** y **Pydantic v2**, probado con **Pytest**.

---

## Características principales

* **API RESTful completa:** Gestión de partidas, ejecución de movimientos con validación de turnos y consulta del estado del tablero.
* **Persistencia de Datos (SQLite):** Guardado automático del estado de las partidas y registro cronológico completo de todos los movimientos realizados (`movimientos`).
* **Lógica de Negocio Inmutable y Robusta:** Mapeo de casillas del **1 al 9**, validación de casillas ocupadas, alternancia estricta de turnos y evaluación automática de victoria/empate.
* **Interfaz Web Interactiva:** Cliente visual integrado accesible vía navegador (`[http://127.0.0.1:8000](http://127.0.0.1:8000)`) con soporte para ratón y **teclado numérico**.
* **Estadísticas globales:** Endpoint dedicado para obtener el cómputo total de partidas jugadas, victorias del Jugador X, victorias del Jugador O y empates.
* **Testing Automatizado:** Suite de pruebas unitarias y de integración con Pytest.

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.12
* **Framework:** FastAPI
* **Servidor:** Uvicorn
* **Base de Datos & ORM:** SQLite / SQLAlchemy
* **Validación de Datos:** Pydantic v2 
* **Testing:** Pytest

---

## 📂 Estructura del Proyecto

```text
Prueba Tres en Raya/
├── app/
│   ├── __init__.py
│   ├── database.py    # Conexión a SQLite y modelos ORM (Game, Movimientos)
│   ├── logic.py       # Lógica pura del juego (validaciones, turnos, victoria/empate)
│   ├── main.py        # Endpoints REST y servidor HTML interactivo
│   └── schemas.py     # Esquemas de validación Pydantic v2
├── tests/
│   └── test_game.py   # Suite de pruebas automatizadas con Pytest
├── .venv/             # Entorno virtual
├── game.db            # Base de datos SQLite (autogenerada)
├── requirements.txt   # Dependencias congeladas del proyecto
└── README.md          # Documentación del proyecto

```

---

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio y acceder al proyecto

```bash
git clone https://github.com/AlejandroBeldaFernandez/Tic-Tac-Toe.git
cd "Prueba Tres en Raya"

```

### 2. Crear y activar el entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate  # En Linux / macOS
# .venv\Scripts\activate   # En Windows

```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt

```

---

## Ejecución de la Aplicación

Para iniciar el servidor de desarrollo con recarga automática:

```bash
uvicorn app.main:app --reload

```

El servidor estará disponible en `[http://127.0.0.1:8000](http://127.0.0.1:8000)`.

* **Interfaz Web:** [http://127.0.0.1:8000](https://www.google.com/url?sa=E&source=gmail&q=http://127.0.0.1:8000)

---

## Ejecución de Tests Automatizados

Para correr la suite completa de pruebas unitarias:

```bash
python -m pytest

```

---

## Documentación de Endpoints y Ejemplos `curl`

### Disposición Mapeada de Casillas (1 a 9)

```text
 1 | 2 | 3 
---+---+---
 4 | 5 | 6 
---+---+---
 7 | 8 | 9 

```

---

### 1. Crear una partida

* **Endpoint:** `POST /partidas`
* **Código de respuesta:** `201 Created`
* **Comando `curl`:**
```bash
curl -X POST "http://127.0.0.1:8000/partidas"

```


* **Respuesta de ejemplo:**
```json
{
  "id": 1,
  "tablero": "*********",
  "turno": "X",
  "estado": "IN_PROGRESS",
  "ganador": null
}

```



---

### 2. Consultar el estado de una partida

* **Endpoint:** `GET /partidas/{id}`
* **Código de respuesta:** `200 OK`
* **Comando `curl`:**
```bash
curl -X GET "http://127.0.0.1:8000/partidas/1"

```



---

### 3. Realizar un movimiento

* **Endpoint:** `POST /partidas/{id}/movimientos`
* **Código de respuesta:** `200 OK`
* **Cuerpo de la petición (JSON):**
```json
{
  "jugador": "X",
  "casilla": 5
}

```


* **Comando `curl`:**
```bash
curl -X POST "http://127.0.0.1:8000/partidas/1/movimientos" \
     -H "Content-Type: application/json" \
     -d '{"jugador": "X", "casilla": 5}'

```



---

### 4. Consultar el historial de movimientos (*Logs*)

* **Endpoint:** `GET /partidas/{id}/logs`
* **Código de respuesta:** `200 OK`
* **Comando `curl`:**
```bash
curl -X GET "http://127.0.0.1:8000/partidas/1/logs"

```


* **Respuesta de ejemplo:**
```json
[
  {
    "id": 1,
    "partida_id": 1,
    "jugador": "X",
    "casilla": 5,
    "timestamp": "2026-11-05T12:00:00"
  }
]

```



---

### 5. Consultar estadísticas globales

* **Endpoint:** `GET /estadisticas`
* **Código de respuesta:** `200 OK`
* **Comando `curl`:**
```bash
curl -X GET "http://127.0.0.1:8000/estadisticas"

```


* **Respuesta de ejemplo:**
```json
{
  "total_partidas": 10,
  "victorias_1": 4,
  "victorias_2": 3,
  "empates": 3
}

```