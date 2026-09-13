from utils.rutas import HTML_DIR
from utils.html_base import crear_pagina_html


def crear_index():

    contenido = """
    <div class="panel-intro">
        <h2 id="reportes-titulo">Tus reportes</h2>
        <p>Ejecutá las herramientas desde la aplicación y consultá los resultados acá.</p>
    </div>

    <section class="checks" aria-labelledby="reportes-titulo">

        <article class="card info">

            <div class="card-top">
                <h2>Diagnóstico</h2>
            </div>

            <p class="resumen">
                Estado general del equipo y puntos a revisar.
            </p>

            <a
                class="panel-link"
                href="diagnostico.html"
            >
                Ver diagnóstico
            </a>

        </article>


        <article class="card info">

            <div class="card-top">
                <h2>Drivers</h2>
            </div>

            <p class="resumen">
                Drivers detectados y copias exportadas.
            </p>

            <a
                class="panel-link"
                href="drivers.html"
            >
                Ver drivers
            </a>

        </article>


        <article class="card info">

            <div class="card-top">
                <h2>Red</h2>
            </div>

            <p class="resumen">
                Configuración de red y estado de la conexión.
            </p>

            <a
                class="panel-link"
                href="red.html"
            >
                Ver red
            </a>

        </article>

        <article class="card info">

            <div class="card-top">
                <h2>Seguridad</h2>
            </div>

            <p class="resumen">
                Resultado de la última revisión de un archivo.
            </p>

            <a
                class="panel-link"
                href="seguridad.html"
            >
                Ver seguridad
            </a>

        </article>

    </section>
    """

    archivo = HTML_DIR / "index.html"

    return crear_pagina_html(
        titulo="Panel",
        subtitulo="Todos los resultados de tus herramientas, en un solo lugar.",
        contenido=contenido,
        archivo=archivo,
        footer="LozTech USB · Panel principal"
    )
