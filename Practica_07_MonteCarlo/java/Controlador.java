import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;

/** CONTROLADOR: ejecuta el modelo, mide tiempos y guarda archivos. */
public class Controlador {
    private static final long SEMILLA = 2026L;
    private static final int[] MUESTRAS = {1000, 10000, 100000, 1000000};
    private static final int REPETICIONES = 3;
    private static final Path RESULTADOS = Path.of("resultados");
    private final MonteCarlo modelo = new MonteCarlo(SEMILLA);
    private final Vista vista = new Vista();

    public void ejecutar() throws IOException {
        Files.createDirectories(RESULTADOS);
        List<String[]> filas = new ArrayList<>();
        List<String> csv = new ArrayList<>();
        csv.add("n,dentro,pi_estimado,error_absoluto,tiempo_segundos");

        for (int n : MUESTRAS) {
            double[] tiempos = new double[REPETICIONES];
            long dentro = 0;
            for (int r = 0; r < REPETICIONES; r++) {
                long inicio = System.nanoTime();
                dentro = modelo.simular(n);
                tiempos[r] = (System.nanoTime() - inicio) / 1_000_000_000.0;
            }
            Arrays.sort(tiempos);
            double pi = modelo.estimarPi(dentro, n);
            String[] fila = {String.valueOf(n), String.valueOf(dentro),
                    String.format(Locale.US, "%.12f", pi),
                    String.format(Locale.US, "%.12f", modelo.errorAbsoluto(pi)),
                    String.format(Locale.US, "%.9f", tiempos[REPETICIONES / 2])};
            filas.add(fila);
            csv.add(String.join(",", fila));
        }
        Files.write(RESULTADOS.resolve("resultados_java.csv"), csv, StandardCharsets.UTF_8);

        List<String> muestra = new ArrayList<>();
        muestra.add("punto,estado_x,x,estado_y,y,dentro");
        for (String[] punto : modelo.primerosPuntos(10)) {
            muestra.add(String.join(",", punto));
        }
        Files.write(RESULTADOS.resolve("secuencia_java.csv"), muestra, StandardCharsets.UTF_8);
        vista.mostrar(filas, SEMILLA, REPETICIONES);
    }
}
