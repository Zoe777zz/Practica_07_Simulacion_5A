/** MODELO: experimento Monte Carlo y generador LCG. */
public class MonteCarlo {
    private static final long MODULO = 2147483647L;
    private static final long MULTIPLICADOR = 16807L;
    private final long semilla;

    public MonteCarlo(long semilla) {
        if (semilla < 1 || semilla >= MODULO) {
            throw new IllegalArgumentException("Semilla invalida");
        }
        this.semilla = semilla;
    }

    private static class GeneradorLCG {
        private long estado;

        GeneradorLCG(long semilla) { this.estado = semilla; }

        long siguienteEstado() {
            estado = (MULTIPLICADOR * estado) % MODULO;
            return estado;
        }
    }

    public long simular(int n) {
        if (n <= 0) { throw new IllegalArgumentException("N debe ser positivo"); }
        GeneradorLCG generador = new GeneradorLCG(semilla);
        long dentro = 0;
        for (int i = 0; i < n; i++) {
            double x = (double) generador.siguienteEstado() / MODULO;
            double y = (double) generador.siguienteEstado() / MODULO;
            if (x * x + y * y <= 1.0) { dentro++; }
        }
        return dentro;
    }

    public double estimarPi(long dentro, int n) { return 4.0 * dentro / n; }
    public double errorAbsoluto(double pi) { return Math.abs(pi - Math.PI); }

    public String[][] primerosPuntos(int cantidad) {
        GeneradorLCG generador = new GeneradorLCG(semilla);
        String[][] puntos = new String[cantidad][6];
        for (int i = 0; i < cantidad; i++) {
            long ex = generador.siguienteEstado();
            long ey = generador.siguienteEstado();
            double x = (double) ex / MODULO;
            double y = (double) ey / MODULO;
            puntos[i] = new String[] {String.valueOf(i + 1), String.valueOf(ex),
                    String.format(java.util.Locale.US, "%.12f", x), String.valueOf(ey),
                    String.format(java.util.Locale.US, "%.12f", y),
                    x * x + y * y <= 1.0 ? "1" : "0"};
        }
        return puntos;
    }
}
