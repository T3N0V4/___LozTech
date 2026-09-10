from html import escape
from pathlib import Path

from utils.assets import (
    cargar_css,
    cargar_js,
    cargar_explosion_random
)


def crear_tarjetas(secciones):
    tarjetas = ""

    for seccion in secciones:
        titulo = escape(
            str(
                seccion.get(
                    "titulo",
                    ""
                )
            )
        )

        contenido = escape(
            str(
                seccion.get(
                    "contenido",
                    ""
                )
            )
        )

        tarjetas += f"""
        <section class="card">
            <h2>{titulo}</h2>
            <pre>{contenido}</pre>
        </section>
        """

    return tarjetas


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

    html_explosion = ""

    if explosion:
        html_explosion = f"""
        <div id="explosion">
            <img
                src="{explosion}"
                alt="BOOM"
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

    <title>
        {escape(str(titulo))}
    </title>

    <style>
        {css}
    </style>

</head>

<body>

    {html_explosion}

    <header>

        <div class="contenido">

            <h1>
                {escape(str(titulo))}
            </h1>

            <p>
                {escape(str(subtitulo))}
            </p>

        </div>

    </header>


    <main>
        {tarjetas}
    </main>


    <footer>
        Generado con LozTech USB
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