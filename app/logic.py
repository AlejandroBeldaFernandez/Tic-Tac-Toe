# Constantes del juego: combinaciones de índices que resultan en victoria
COMBINACIONES_GANADORAS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
    [0, 4, 8], [2, 4, 6]              # Diagonales
]

def verificar_ganador(tablero: list[str]) -> bool:
    """
    Recorre las 8 combinaciones ganadoras.
    Retorna True si alguna combinación tiene 3 fichas iguales distintas de '*'.
    """
    for a, b, c in COMBINACIONES_GANADORAS:
        if tablero[a] == tablero[b] == tablero[c] != "*":
            return True
    return False

def verificar_empate(tablero: list[str]) -> bool:
    """
    Comprueba si el tablero está lleno ('*' no presente) sin que haya ningún ganador.
    """
    return "*" not in tablero and not verificar_ganador(tablero)

def marcar_casilla(jugador: str, casilla: int, tablero: list[str], jugador_actual: str) -> list[str]:
    """
    Valida las reglas de negocio antes de aplicar el movimiento:
    1. Verifica que sea el turno del jugador correspondiente.
    2. Verifica que la casilla esté en el rango permitido (0 a 8).
    3. Verifica que la casilla no esté ya ocupada.
    Lanza ValueError si alguna regla se incumple.
    """
    if jugador != jugador_actual:
        raise ValueError(f"No es el turno de {jugador}. Le toca a {jugador_actual}.")

    if casilla < 1 or casilla > 9:
        raise ValueError("La casilla debe estar entre 1 y 9.")

    if tablero[casilla - 1] != "*":
        raise ValueError("La casilla ya está ocupada.")

    # Retorna una copia del tablero con la jugada aplicada
    nuevo_tablero = tablero.copy()
    nuevo_tablero[casilla - 1] = jugador
    return nuevo_tablero