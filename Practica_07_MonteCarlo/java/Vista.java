import java.util.List;
import java.util.Locale;

/** VISTA: presenta la tabla en consola. */
public class Vista {
    public void mostrar(List<String[]> filas, long semilla, int repeticiones) {
        System.out.println("MONTE CARLO - JAVA");
        System.out.println("Semilla: " + semilla + " | Repeticiones por N: " + repeticiones);
        System.out.printf("%10s %10s %14s %13s %13s%n", "N", "Dentro", "Pi estimado", "Error abs.", "Tiempo (s)");
        for (String[] f : filas) {
            System.out.printf(Locale.US, "%,10d %,10d %14.9f %13.9f %13.6f%n",
                    Integer.parseInt(f[0]), Long.parseLong(f[1]), Double.parseDouble(f[2]),
                    Double.parseDouble(f[3]), Double.parseDouble(f[4]));
        }
        System.out.println("\nCSV guardados en resultados/.");
    }
}
