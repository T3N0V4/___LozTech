from html import escape

from utils.rutas import HTML_DIR
from utils.html_base import crear_pagina_html


def bytes_a_mb(bytes_totales):
    return round(
        bytes_totales / (1024 * 1024),
        2
    )


def crear_html_seguridad(resultado):
    vt = resultado.get(
        "virustotal"
    )

    if vt is None:
        estado = "info"
        titulo_estado = "Sin reporte previo"

        resumen_vt = """
        VirusTotal no encontró un análisis previo
        para este archivo.
        """

        detalles_vt = """
        No se subió el archivo.
        Solo se consultó su SHA-256.
        """

    else:
        malicious = vt.get(
            "malicious",
            0
        )

        suspicious = vt.get(
            "suspicious",
            0
        )

        harmless = vt.get(
            "harmless",
            0
        )

        undetected = vt.get(
            "undetected",
            0
        )

        total = (
            malicious
            + suspicious
            + harmless
            + undetected
        )

        if malicious > 0:
            estado = "error"
            titulo_estado = (
                "Se detectaron amenazas"
            )

        elif suspicious > 0:
            estado = "warning"
            titulo_estado = (
                "Archivo sospechoso"
            )

        else:
            estado = "ok"
            titulo_estado = (
                "Sin detecciones conocidas"
            )

        resumen_vt = (
            f"{malicious} detecciones maliciosas "
            f"de {total} motores."
        )

        detalles_vt = f"""
Maliciosos: {malicious}
Sospechosos: {suspicious}
Inofensivos: {harmless}
Sin detección: {undetected}
        """.strip()

    contenido = f"""
    <section class="summary">

        <div>
            <span class="summary-label">
                Resultado
            </span>

            <h2 class="{estado}">
                {escape(titulo_estado)}
            </h2>
        </div>

    </section>


    <section class="checks">

        <article class="card info">

            <div class="card-top">

                <h2>
                    Archivo
                </h2>

                <span class="badge info">
                    Información
                </span>

            </div>

            <p class="resumen">
                {escape(resultado["nombre"])}
            </p>

            <details open>

                <summary>
                    Ver detalles
                </summary>

                <pre>Ruta: {escape(resultado["ruta"])}
Tamaño: {bytes_a_mb(resultado["tamano"])} MB
SHA-256: {escape(resultado["sha256"])}</pre>

            </details>

        </article>


        <article class="card {estado}">

            <div class="card-top">

                <h2>
                    VirusTotal
                </h2>

                <span class="badge {estado}">
                    {escape(titulo_estado)}
                </span>

            </div>

            <p class="resumen">
                {escape(resumen_vt.strip())}
            </p>

            <details open>

                <summary>
                    Ver detalles
                </summary>

                <pre>{escape(detalles_vt)}</pre>

            </details>

        </article>

    </section>
    """

    archivo = (
        HTML_DIR
        / "seguridad.html"
    )

    return crear_pagina_html(
        titulo="Seguridad",
        subtitulo=(
            "Análisis de reputación de archivos."
        ),
        contenido=contenido,
        archivo=archivo,
        footer=(
            "LozTech USB · "
            "Análisis de seguridad"
        )
    )