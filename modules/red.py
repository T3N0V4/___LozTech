from html import escape

from utils.comandos import ejecutar
from utils.rutas import HTML_DIR
from utils.html_base import crear_pagina_html


def diagnosticar_red():

    configuracion = ejecutar(
        "ipconfig /all"
    )

    ping = ejecutar(
        "ping 8.8.8.8 -n 4"
    )

    dns = ejecutar(
        "nslookup google.com"
    )

    contenido = f"""
    <section class="checks">

        <article class="card info">

            <div class="card-top">

                <h2>
                    Configuración de red
                </h2>

                <span class="badge info">
                    Información
                </span>

            </div>

            <details open>

                <summary>
                    Ver configuración
                </summary>

                <pre>{escape(configuracion)}</pre>

            </details>

        </article>


        <article class="card info">

            <div class="card-top">

                <h2>
                    Conectividad
                </h2>

                <span class="badge info">
                    Información
                </span>

            </div>

            <details open>

                <summary>
                    Ver resultado
                </summary>

                <pre>{escape(ping)}</pre>

            </details>

        </article>


        <article class="card info">

            <div class="card-top">

                <h2>
                    DNS
                </h2>

                <span class="badge info">
                    Información
                </span>

            </div>

            <details open>

                <summary>
                    Ver resultado
                </summary>

                <pre>{escape(dns)}</pre>

            </details>

        </article>

    </section>
    """

    archivo = (
        HTML_DIR
        / "red.html"
    )

    return crear_pagina_html(
        titulo="Diagnóstico de red",
        subtitulo=(
            "Configuración, conectividad "
            "y resolución DNS."
        ),
        contenido=contenido,
        archivo=archivo,
        footer=(
            "LozTech USB · "
            "Diagnóstico de red local"
        )
    )