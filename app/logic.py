COMBINACIONES_GANADORAS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
    [0, 4, 8], [2, 4, 6]              # Diagonales
]

def verificar_ganador(tablero: list[str]) -> bool:
    for a, b, c in COMBINACIONES_GANADORAS:
        if tablero[a] == tablero[b] == tablero[c] != "*":
            return True
    return False    

def verificar_empate(tablero: list[str]) -> bool:
    return "*" not in tablero and not verificar_ganador(tablero)

def marcar_casilla(jugador: str, casilla: int, tablero: list[str]) -> list[str]:

    if casilla < 0 or casilla > 8:
        raise ValueError("La casilla debe estar entre 0 y 8 (o 1 y 9 según la vista).")
    
    if tablero[casilla] != "*":
        raise ValueError("Casilla ocupada. Por favor, elige otra casilla.")
    
    nuevo_tablero = tablero.copy()
    nuevo_tablero[casilla] = jugador
    return nuevo_tablero