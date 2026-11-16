"""Entrada del programa. Ejecuta unicamente la opcion solicitada."""

import argparse
from controlador import Controlador


def main() -> None:
    parser = argparse.ArgumentParser(description="Practica 07 - Monte Carlo MVC")
    parser.add_argument("opcion", nargs="?", choices=["ejecutar", "comparar", "graficar"],
                        default="ejecutar", help="Accion (por defecto: ejecutar)")
    opcion = parser.parse_args().opcion
    controlador = Controlador()
    if opcion == "ejecutar":
        controlador.ejecutar()
    elif opcion == "comparar":
        controlador.comparar()
    else:
        controlador.graficar()


if __name__ == "__main__":
    main()
