import hashlib
import json

from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from utils.rutas import APP_DIR


VT_KEY_FILE = APP_DIR / "virustotal.key"


def calcular_sha256(archivo):
    hash_sha256 = hashlib.sha256()

    with open(archivo, "rb") as archivo_abierto:

        for bloque in iter(
            lambda: archivo_abierto.read(1024 * 1024),
            b""
        ):
            hash_sha256.update(bloque)

    return hash_sha256.hexdigest()


def cargar_api_key():
    if not VT_KEY_FILE.exists():
        raise RuntimeError(
            "No se encontró virustotal.key."
        )

    api_key = VT_KEY_FILE.read_text(
        encoding="utf-8"
    ).strip()

    if not api_key:
        raise RuntimeError(
            "virustotal.key está vacío."
        )

    return api_key


def consultar_virustotal(hash_archivo):
    api_key = cargar_api_key()

    url = (
        "https://www.virustotal.com/"
        f"api/v3/files/{hash_archivo}"
    )

    request = Request(
        url,
        headers={
            "x-apikey": api_key
        }
    )

    try:

        with urlopen(
            request,
            timeout=15
        ) as respuesta:

            datos = json.loads(
                respuesta.read()
                .decode("utf-8")
            )

            return datos

    except HTTPError as error:

        if error.code == 404:
            return None

        if error.code == 429:
            raise RuntimeError(
                "Límite de consultas de VirusTotal alcanzado."
            )

        raise RuntimeError(
            f"VirusTotal respondió HTTP {error.code}."
        )

    except URLError:
        raise RuntimeError(
            "No se pudo conectar con VirusTotal."
        )


def analizar_archivo(archivo):
    archivo = Path(archivo)

    sha256 = calcular_sha256(
        archivo
    )

    resultado = {
        "nombre": archivo.name,
        "ruta": str(archivo),
        "tamano": archivo.stat().st_size,
        "sha256": sha256,
        "virustotal": None
    }

    datos = consultar_virustotal(
        sha256
    )

    if datos:

        atributos = (
            datos
            .get("data", {})
            .get("attributes", {})
        )

        estadisticas = atributos.get(
            "last_analysis_stats",
            {}
        )

        resultado["virustotal"] = {
            "malicious": estadisticas.get(
                "malicious",
                0
            ),
            "suspicious": estadisticas.get(
                "suspicious",
                0
            ),
            "harmless": estadisticas.get(
                "harmless",
                0
            ),
            "undetected": estadisticas.get(
                "undetected",
                0
            )
        }

    return resultado