from modules.seguridad.archivo import (
    obtener_datos_archivo
)

from modules.seguridad.virustotal import (
    consultar_virustotal
)


def analizar_archivo(archivo):

    resultado = obtener_datos_archivo(
        archivo
    )

    sha256 = (
        resultado["hashes"]["sha256"]
    )

    resultado["virustotal"] = None

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
            "malicious":
                estadisticas.get(
                    "malicious",
                    0
                ),

            "suspicious":
                estadisticas.get(
                    "suspicious",
                    0
                ),

            "harmless":
                estadisticas.get(
                    "harmless",
                    0
                ),

            "undetected":
                estadisticas.get(
                    "undetected",
                    0
                )
        }

    return resultado