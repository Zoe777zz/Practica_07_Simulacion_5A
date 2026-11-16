"""MODELO: numeros pseudoaleatorios y estimacion de pi con Monte Carlo."""

import math

MODULO = 2_147_483_647
MULTIPLICADOR = 16_807


class GeneradorLCG:
    """Genera valores U en (0, 1) de manera reproducible."""

    def __init__(self, semilla: int):
        if not 1 <= semilla < MODULO:
            raise ValueError("La semilla debe estar entre 1 y MODULO - 1")
        self.estado = semilla

    def siguiente(self) -> tuple[int, float]:
        self.estado = (MULTIPLICADOR * self.estado) % MODULO
        return self.estado, self.estado / MODULO


class MonteCarlo:
    """Contiene el experimento y las formulas, sin imprimir ni guardar archivos."""

    def __init__(self, semilla: int = 2026):
        self.semilla = semilla

    def simular(self, n: int) -> int:
        if n <= 0:
            raise ValueError("N debe ser positivo")
        generador = GeneradorLCG(self.semilla)
        dentro = 0
        for _ in range(n):
            _, x = generador.siguiente()
            _, y = generador.siguiente()
            if x * x + y * y <= 1:
                dentro += 1
        return dentro

    @staticmethod
    def estimar_pi(dentro: int, n: int) -> float:
        return 4 * dentro / n

    @staticmethod
    def error_absoluto(estimacion: float) -> float:
        return abs(estimacion - math.pi)

    def primeros_puntos(self, cantidad: int = 10) -> list[tuple]:
        generador = GeneradorLCG(self.semilla)
        puntos = []
        for i in range(1, cantidad + 1):
            estado_x, x = generador.siguiente()
            estado_y, y = generador.siguiente()
            dentro = int(x * x + y * y <= 1)
            puntos.append((i, estado_x, f"{x:.12f}", estado_y, f"{y:.12f}", dentro))
        return puntos
