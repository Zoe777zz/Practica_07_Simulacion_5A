"""VISTA: salida de consola y graficas. Sin calculos del experimento."""

from pathlib import Path


class Vista:
    @staticmethod
    def tabla(lenguaje: str, filas: list[dict], semilla: int, repeticiones: int) -> None:
        print(f"MONTE CARLO - {lenguaje.upper()}")
        print(f"Semilla: {semilla} | Repeticiones por N: {repeticiones}")
        print(f"{'N':>10} {'Dentro':>10} {'Pi estimado':>14} {'Error abs.':>13} {'Tiempo (s)':>13}")
        for fila in filas:
            print(f"{fila['n']:>10,} {fila['dentro']:>10,} "
                  f"{fila['pi_estimado']:>14.9f} {fila['error_absoluto']:>13.9f} "
                  f"{fila['tiempo_segundos']:>13.6f}")
        print("\nCSV guardados en resultados/.")

    @staticmethod
    def comparacion(filas: list[dict]) -> None:
        print("COMPARACION PYTHON / JAVA (tiempos en segundos)")
        print(f"{'N':>10} {'Pi':>13} {'Error':>12} {'Python':>12} {'Java':>12} {'Mas rapido':>12}")
        for f in filas:
            print(f"{int(f['n']):>10,} {float(f['pi_estimado']):>13.9f} "
                  f"{float(f['error_absoluto']):>12.9f} "
                  f"{float(f['tiempo_python_segundos']):>12.6f} "
                  f"{float(f['tiempo_java_segundos']):>12.6f} {f['mas_rapido']:>12}")
        print("\nVerificacion correcta: secuencias y estimaciones coinciden.")

    @staticmethod
    def graficar(filas: list[dict], destino: Path) -> None:
        """Matplotlib se necesita solo si se solicitan graficas."""
        import math
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        destino.mkdir(parents=True, exist_ok=True)
        etiquetas = [f"{int(f['n']):,}".replace(",", " ") for f in filas]
        x = list(range(len(filas)))
        pi = [float(f['pi_estimado']) for f in filas]
        errores = [float(f['error_absoluto']) for f in filas]
        python = [float(f['tiempo_python_segundos']) for f in filas]
        java = [float(f['tiempo_java_segundos']) for f in filas]
        azul, celeste = "#214578", "#78A7D9"
        plt.rcParams.update({"font.size": 10, "figure.dpi": 140, "axes.spines.top": False,
                             "axes.spines.right": False})

        fig, ax = plt.subplots(figsize=(8, 3.6))
        ax.plot(x, pi, "o-", color=azul, label="Estimacion Monte Carlo")
        ax.axhline(math.pi, linestyle="--", color=celeste, label="Valor de pi")
        ax.set_xticks(x, etiquetas)
        ax.set(xlabel="Numero de puntos (N)", ylabel="Valor estimado", title="Aproximacion de pi")
        ax.grid(axis="y", alpha=.2)
        ax.legend(frameon=False)
        fig.tight_layout()
        fig.savefig(destino / "convergencia_pi.png")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(8, 3.6))
        ax.bar(x, errores, width=.55, color=azul)
        ax.set_xticks(x, etiquetas)
        ax.set(xlabel="Numero de puntos (N)", ylabel="Error absoluto", title="Error absoluto de la estimacion")
        ax.grid(axis="y", alpha=.2)
        fig.tight_layout()
        fig.savefig(destino / "error_absoluto.png")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(8, 3.6))
        ancho = .34
        ax.bar([i - ancho / 2 for i in x], python, width=ancho, color=azul, label="Python")
        ax.bar([i + ancho / 2 for i in x], java, width=ancho, color=celeste, label="Java")
        ax.set_xticks(x, etiquetas)
        ax.set(xlabel="Numero de puntos (N)", ylabel="Tiempo (s)", title="Tiempo de ejecucion por lenguaje")
        ax.grid(axis="y", alpha=.2)
        ax.legend(frameon=False)
        fig.tight_layout()
        fig.savefig(destino / "comparacion_tiempos.png")
        plt.close(fig)
        print("Graficas guardadas en resultados/.")
