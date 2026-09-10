from utils.comandos import ejecutar
from utils.rutas import DRIVERS_DIR


def exportar_drivers():

    comando = (
        f'pnputil /export-driver * '
        f'"{DRIVERS_DIR}"'
    )

    ejecutar(comando)

    return DRIVERS_DIR