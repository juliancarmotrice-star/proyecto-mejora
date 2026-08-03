"""Calcula el tiempo promedio por estación a partir de datos/tiempos.csv."""

from collections import defaultdict
from pathlib import Path

RUTA_DATOS = Path("datos") / "tiempos.csv"


def leer_tiempos(ruta: Path) -> dict[str, list[float]]:
    """Lee el CSV y agrupa los tiempos (segundos) por estación."""
    tiempos_por_estacion: dict[str, list[float]] = defaultdict(list)

    with ruta.open(encoding="utf-8") as archivo:
        for indice, linea in enumerate(archivo):
            # Cada fila del archivo viene entre comillas: "estacion,operacion,tiempo"
            campos = [c.strip() for c in linea.strip().strip('"').split(",")]
            if not campos or len(campos) < 3:
                continue
            if indice == 0:
                continue  # encabezado

            estacion = campos[0]
            tiempo = float(campos[2])
            tiempos_por_estacion[estacion].append(tiempo)

    return tiempos_por_estacion


def promedios_por_estacion(
    tiempos_por_estacion: dict[str, list[float]],
) -> dict[str, float]:
    """Devuelve el promedio de tiempo por estación."""
    return {
        estacion: sum(tiempos) / len(tiempos)
        for estacion, tiempos in tiempos_por_estacion.items()
    }


def main() -> None:
    if not RUTA_DATOS.exists():
        raise SystemExit(f"No se encontró el archivo de datos: {RUTA_DATOS}")

    tiempos = leer_tiempos(RUTA_DATOS)
    promedios = promedios_por_estacion(tiempos)

    print("Tiempo promedio por estación (segundos):")
    for estacion in sorted(promedios, key=lambda e: int(e)):
        print(f"  Estación {estacion}: {promedios[estacion]:.2f}")


if __name__ == "__main__":
    main()
