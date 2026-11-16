
# Practica 07 - Monte Carlo 

**Asignatura:** Simulacion | **Sistema:** Ubuntu / Debian | **Arquitectura:** Modelo-Vista-Controlador (MVC)

Se estima pi con puntos `(x, y)` en el cuadrado unitario y se cuentan los que cumplen `x*x + y*y <= 1`.

`pi_estimado = 4 * puntos_dentro / N`

Se trabaja con `N = 1000, 10000, 100000, 1000000`, semilla `2026` y **3 mediciones de tiempo por N** (mediana). Python y Java usan el mismo LCG y generan los mismos resultados numericos.

## 1. Estructura MVC

```text
Practica_07_MonteCarlo/
├── python/
│   ├── monte_carlo.py    # Modelo: GeneradorLCG y MonteCarlo
│   ├── vista.py          # Vista: tabla y graficas
│   ├── controlador.py    # Controlador: experimento, CSV y comparacion
│   └── main.py           # Inicio de Python
├── java/
│   ├── MonteCarlo.java   # Modelo: LCG y Monte Carlo
│   ├── Vista.java        # Vista: tabla en consola
│   ├── Controlador.java  # Controlador: tiempos y CSV
│   └── Main.java         # Inicio de Java
├── resultados/           # CSV y graficas
├── requirements.txt
├── .gitignore
└── README.md
```

La **vista grafica se hace en Python** con Matplotlib, a partir de los CSV de ambos lenguajes. Asi no se repiten graficas en Java y Python.

## 2. Instalar lo basico en Ubuntu

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip openjdk-17-jdk
```

## 3. Clonar desde GitHub

Cuando publiques tu proyecto, usa su enlace real:

```bash
git clone URL_REAL_DEL_REPOSITORIO
cd NOMBRE_DE_LA_CARPETA_CLONADA
```

Si ya descargaste el ZIP, abre una terminal **dentro de la carpeta que contiene `README.md`, `python/` y `java/`**. No es necesario volver a descargarlo para ejecutar los comandos siguientes.

## 4. Ejecutar (desde la raiz del proyecto)

```bash
# 1. Python
python3 python/main.py

# 2. Java
mkdir -p build
javac -d build java/*.java
java -cp build Main

# 3. Comparar: confirma mismas secuencias y estimaciones
python3 python/main.py comparar
```

Se generan `resultados_python.csv`, `resultados_java.csv`, los dos archivos `secuencia_*.csv` y `comparacion.csv`, todos dentro de `resultados/`.

## 5. Generar graficas sin el error de pip de Ubuntu

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python python/main.py graficar
```

Se guardan: `convergencia_pi.png`, `error_absoluto.png` y `comparacion_tiempos.png`.

Para volver a trabajar otro dia: `source .venv/bin/activate`. Para salir: `deactivate`.

## 6. Que hace cada parte

- **Modelo (`monte_carlo.py` y `MonteCarlo.java`):** genera puntos con el LCG, cuenta los que caen en el cuarto de circulo y calcula pi y el error.
- **Vista (`vista.py` y `Vista.java`):** presenta los resultados; la vista Python tambien dibuja las tres graficas.
- **Controlador (`controlador.py` y `Controlador.java`):** selecciona las muestras, cronometra las ejecuciones, guarda CSV y solicita la salida a la vista. Python tambien verifica la equivalencia entre lenguajes.
- **Main (`main.py` y `Main.java`):** arranca el controlador, sin repetir el algoritmo.

**Nota:** los conteos y las estimaciones coinciden entre Python y Java; los tiempos dependen de cada equipo y ejecucion. La guia solicita comparar ambos, no que sus tiempos sean iguales.
