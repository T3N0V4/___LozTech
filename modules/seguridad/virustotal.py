import json

from urllib.request import (
    Request,
    urlopen
)

from urllib.error import (
    HTTPError,
    URLError
)

from utils.rutas import APP_DIR


VT_KEY_FILE = (
    APP_DIR
    / "virustotal.key"
)


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


def consultar_virustotal(
    hash_archivo
):

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

            return json.loads(
                respuesta
                .read()
                .decode("utf-8")
            )

    except HTTPError as error:

        if error.code == 404:
            return None

        if error.code == 429:
            raise RuntimeError(
                "Límite de consultas "
                "de VirusTotal alcanzado."
            )

        raise RuntimeError(
            f"VirusTotal respondió HTTP "
            f"{error.code}."
        )

    except URLError:

        raise RuntimeError(
            "No se pudo conectar "
            "con VirusTotal."
        )