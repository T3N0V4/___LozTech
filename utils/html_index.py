from utils.rutas import HTML_DIR
from utils.html_base import crear_pagina_html


def crear_index():

    contenido = """
    <section class="checks">

        <article class="card info">

            <div class="card-top">
                <h2>Diagnóstico</h2>
            </div>

            <p class="resumen">
                Revisar estado general del sistema.
            </p>

            <a
                class="panel-link"
                href="diagnostico.html"
            >
                Abrir diagnóstico
            </a>

        </article>


        <article class="card info">

            <div class="card-top">
                <h2>Drivers</h2>
            </div>

            <p class="resumen">
                Ver drivers detectados y exportados.
            </p>

            <a
                class="panel-link"
                href="drivers.html"
            >
                Abrir drivers
            </a>

        </article>


        <article class="card info">

            <div class="card-top">
                <h2>Red</h2>
            </div>

            <p class="resumen">
                Revisar configuración y conectividad.
            </p>

            <a
                class="panel-link"
                href="red.html"
            >
                Abrir red
            </a>

        </article>

    </section>
    """

    archivo = HTML_DIR / "index.html"

    return crear_pagina_html(
        titulo="Panel",
        subtitulo="Herramientas y reportes de LozTech.",
        contenido=contenido,
        archivo=archivo,
        footer="LozTech USB · Panel principal"
    )