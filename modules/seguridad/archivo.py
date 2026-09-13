import hashlib
from pathlib import Path


def calcular_hash(archivo, algoritmo):
    hash_obj = hashlib.new(
        algoritmo
    )

    with open(archivo, "rb") as archivo_abierto:

        for bloque in iter(
            lambda: archivo_abierto.read(
                1024 * 1024
            ),
            b""
        ):
            hash_obj.update(
                bloque
            )

    return hash_obj.hexdigest()


def obtener_datos_archivo(archivo):
    archivo = Path(
        archivo
    )

    return {
        "nombre": archivo.name,
        "ruta": str(archivo),
        "tamano": archivo.stat().st_size,
        "extension": archivo.suffix.lower(),

        "hashes": {
            "md5": calcular_hash(
                archivo,
                "md5"
            ),

            "sha1": calcular_hash(
                archivo,
                "sha1"
            ),

            "sha256": calcular_hash(
                archivo,
                "sha256"
            )
        }
    }