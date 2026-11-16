"""CONTROLADOR: coordina modelo, vista, archivos y mediciones."""

import csv
import statistics
import time
from pathlib import Path

from monte_carlo import MonteCarlo
from vista import Vista

RESULTADOS = Path(__file__).resolve().parent.parent / "resultados"
SEMILLA = 2026
MUESTRAS = (1_000, 10_000, 100_000, 1_000_000)
REPETICIONES = 3


class Controlador:
    def __init__(self):
        self.modelo = MonteCarlo(SEMILLA)
        RESULTADOS.mkdir(exist_ok=True)

    @staticmethod
    def guardar_csv(nombre: str, campos: list[str], filas: list) -> None:
        with (RESULTADOS / nombre).open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(campos)
            escritor.writerows(filas)

    @staticmethod
    def leer_csv(nombre: str) -> list[dict]:
        ruta = RESULTADOS / nombre
        if not ruta.exists():
            raise FileNotFoundError(f"Falta {nombre}. Ejecuta primero Python y Java.")
        with ruta.open(newline="", encoding="utf-8") as archivo:
            return list(csv.DictReader(archivo))

    def ejecutar(self) -> None:
        filas = []
        for n in MUESTRAS:
            tiempos = []
            for _ in range(REPETICIONES):
                inicio = time.perf_counter()
                dentro = self.modelo.simular(n)
                tiempos.append(time.perf_counter() - inicio)
            pi = self.modelo.estimar_pi(dentro, n)
            filas.append({"n": n, "dentro": dentro, "pi_estimado": pi,
                          "error_absoluto": self.modelo.error_absoluto(pi),
                          "tiempo_segundos": statistics.median(tiempos)})

        campos = ["n", "dentro", "pi_estimado", "error_absoluto", "tiempo_segundos"]
        self.guardar_csv("resultados_python.csv", campos,
                         [[f['n'], f['dentro'], f"{f['pi_estimado']:.12f}",
                           f"{f['error_absoluto']:.12f}", f"{f['tiempo_segundos']:.9f}"] for f in filas])
        self.guardar_csv("secuencia_python.csv",
                         ["punto", "estado_x", "x", "estado_y", "y", "dentro"],
                         self.modelo.primeros_puntos())
        Vista.tabla("Python", filas, SEMILLA, REPETICIONES)

    def comparar(self) -> None:
        python = self.leer_csv("resultados_python.csv")
        java = self.leer_csv("resultados_java.csv")
        if len(python) != len(java) or self.leer_csv("secuencia_python.csv") != self.leer_csv("secuencia_java.csv"):
            raise AssertionError("Las secuencias o las cantidades de filas difieren")
        filas = []
        for p, j in zip(python, java):
            if any(p[c] != j[c] for c in ("n", "dentro", "pi_estimado", "error_absoluto")):
                raise AssertionError(f"Resultados diferentes para N={p['n']}")
            tp, tj = float(p["tiempo_segundos"]), float(j["tiempo_segundos"])
            filas.append({"n": p["n"], "dentro": p["dentro"],
                          "pi_estimado": p["pi_estimado"], "error_absoluto": p["error_absoluto"],
                          "tiempo_python_segundos": p["tiempo_segundos"],
                          "tiempo_java_segundos": j["tiempo_segundos"],
                          "mas_rapido": "Python" if tp < tj else "Java" if tj < tp else "Empate"})
        campos = ["n", "dentro", "pi_estimado", "error_absoluto",
                  "tiempo_python_segundos", "tiempo_java_segundos", "mas_rapido"]
        self.guardar_csv("comparacion.csv", campos, [[f[c] for c in campos] for f in filas])
        Vista.comparacion(filas)

    def graficar(self) -> None:
        Vista.graficar(self.leer_csv("comparacion.csv"), RESULTADOS)
