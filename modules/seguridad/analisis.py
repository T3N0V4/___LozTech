from modules.seguridad.archivo import obtener_datos_archivo
from modules.seguridad.virustotal import consultar_virustotal
from modules.seguridad.antivirus import obtener_antivirus
from modules.seguridad.defender import obtener_informacion_defender
from modules.seguridad.avg import obtener_informacion_avg


def detectar_proveedores_antivirus(antivirus):
    proveedores = set()

    for producto in antivirus:
        nombre = producto.get(
            "nombre",
            ""
        ).lower()

        if "avg" in nombre:
            proveedores.add("avg")

        if (
            "defender" in nombre
            or "microsoft" in nombre
        ):
            proveedores.add("defender")

    return proveedores


def obtener_seguridad_sistema():
    antivirus = obtener_antivirus()

    proveedores = detectar_proveedores_antivirus(
        antivirus
    )

    seguridad = {
        "antivirus": antivirus,
        "proveedores": list(proveedores),
        "defender": None,
        "avg": None
    }

    if "defender" in proveedores:
        seguridad["defender"] = (
            obtener_informacion_defender()
        )

    if "avg" in proveedores:
        seguridad["avg"] = (
            obtener_informacion_avg()
        )

    return seguridad


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

    resultado["seguridad"] = (
        obtener_seguridad_sistema()
    )

    return resultado