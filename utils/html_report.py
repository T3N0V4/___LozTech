from html import escape
from pathlib import Path

from utils.assets import (
    cargar_css,
    cargar_js,
    cargar_explosion_random
)


def crear_tarjetas(secciones):
    tarjetas = ""

    nombres_estado = {
        "ok": "Correcto",
        "warning": "Atención",
        "error": "Problema",
        "info": "Información"
    }

    for seccion in secciones:
        titulo = escape(
            str(seccion.get("titulo", ""))
        )

        resumen = escape(
            str(seccion.get("resumen", ""))
        )

        detalles = escape(
            str(seccion.get("detalles", ""))
        )

        estado = seccion.get(
            "estado",
            "info"
        )

        nombre_estado = nombres_estado.get(
            estado,
            "Información"
        )

        progreso = seccion.get(
            "progreso"
        )

        barra = ""

        if progreso is not None:
            progreso = max(
                0,
                min(100, progreso)
            )

            barra = f"""
            <div class="progress">
                <div
                    class="progress-value {estado}"
                    style="width: {progreso}%"
                ></div>
            </div>

            <div class="progress-number">
                {progreso}%
            </div>
            """

        detalles_html = ""

        if detalles:
            detalles_html = f"""
            <details>
                <summary>Ver detalles</summary>

                <pre>{detalles}</pre>
            </details>
            """

        tarjetas += f"""
        <article class="card {estado}">

            <div class="card-top">

                <h2>{titulo}</h2>

                <span class="badge {estado}">
                    {nombre_estado}
                </span>

            </div>

            <p class="resumen">
                {resumen}
            </p>

            {barra}

            {detalles_html}

        </article>
        """

    return tarjetas


def crear_resumen(secciones):
    conteos = {
        "ok": 0,
        "warning": 0,
        "error": 0,
        "info": 0
    }

    for seccion in secciones:
        estado = seccion.get(
            "estado",
            "info"
        )

        conteos[estado] = (
            conteos.get(estado, 0)
            + 1
        )

    if conteos["error"] > 0:
        estado_general = "Se detectaron problemas"
        clase = "error"

    elif conteos["warning"] > 0:
        estado_general = "Hay elementos para revisar"
        clase = "warning"

    else:
        estado_general = "No se detectaron problemas importantes"
        clase = "ok"

    return f"""
    <section class="summary">

        <div>
            <span class="summary-label">
                Resultado
            </span>

            <h2 class="{clase}">
                {estado_general}
            </h2>
        </div>

        <div class="summary-stats">

            <div>
                <strong>{conteos["ok"]}</strong>
                <span>Correctos</span>
            </div>

            <div>
                <strong>{conteos["warning"]}</strong>
                <span>Atención</span>
            </div>

            <div>
                <strong>{conteos["error"]}</strong>
                <span>Problemas</span>
            </div>

        </div>

    </section>
    """


def crear_reporte_html(
    titulo,
    subtitulo,
    secciones,
    archivo: Path
):
    css = cargar_css()
    js = cargar_js()

    explosion = cargar_explosion_random()

    tarjetas = crear_tarjetas(
        secciones
    )

    resumen = crear_resumen(
        secciones
    )

    html_explosion = ""

    if explosion:
        html_explosion = f"""
        <div id="explosion">
            <img
                src="{explosion}"
                alt=""
            >
        </div>
        """

    html = f"""
<!DOCTYPE html>

<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>{escape(str(titulo))}</title>

    <style>
        {css}
    </style>

</head>

<body>

    {html_explosion}

        <header>

        <div class="container">

            <div class="header-top">

                <div class="brand">
                    LOZTECH
                </div>

                <select
                    id="theme-selector"
                    class="theme-selector"
                    aria-label="Tema"
                >
                    <option value="black">
                        Black
                    </option>

                    <option value="blue">
                        Blue
                    </option>

                    <option value="violet">
                        Violet
                    </option>

                    <option value="cosmos">
                        Cosmos
                    </option>

                    <option value="grey">
                        Grey
                    </option>
                </select>

            </div>

            <h1>
                {escape(str(titulo))}
            </h1>

            <p>
                {escape(str(subtitulo))}
            </p>

        </div>

    </header>


    <main class="container">

        {resumen}

        <section class="checks">
            {tarjetas}
        </section>

    </main>


    <footer>
        LozTech USB · Reporte generado localmente
    </footer>


    <script>
        {js}
    </script>

</body>

</html>
"""

    archivo.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    archivo.write_text(
        html,
        encoding="utf-8"
    )

    return archivo