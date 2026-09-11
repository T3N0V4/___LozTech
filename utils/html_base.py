from html import escape
from pathlib import Path

from utils.assets import (
    cargar_css,
    cargar_js,
    cargar_explosion_random
)


def crear_pagina_html(
    titulo,
    subtitulo,
    contenido,
    archivo: Path,
    footer="LozTech USB · Generado localmente"
):
    pagina = archivo.stem
    css = cargar_css(pagina)
    js = cargar_js(pagina)

    explosion = cargar_explosion_random() if pagina == "index" else None

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

    <title>
        {escape(str(titulo))}
    </title>

    <style>
        {css}
    </style>

</head>

<body data-page="{escape(pagina, quote=True)}">

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


            <nav class="nav">

                <a href="index.html">
                    Inicio
                </a>

                <a href="diagnostico.html">
                    Diagnóstico
                </a>

                <a href="drivers.html">
                    Drivers
                </a>

                <a href="red.html">
                    Red
                </a>

            </nav>


            <h1>
                {escape(str(titulo))}
            </h1>

            <p>
                {escape(str(subtitulo))}
            </p>

        </div>

    </header>


    <main class="container">

        {contenido}

    </main>


    <footer>
        {escape(str(footer))}
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
        encoding="utf-8",
        newline="\n"
    )

    return archivo
