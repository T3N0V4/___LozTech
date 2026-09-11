import base64
import random
import os
from utils.rutas import BASE_DIR


CSS_DIR = (
    BASE_DIR
    / "assets"
    / "css"
)


JS_DIR = (
    BASE_DIR
    / "assets"
    / "js"
)


EXPLOSIONES_DIR = (
    BASE_DIR
    / "assets"
    / "explosiones"
)


def cargar_css(pagina=None):

    if not CSS_DIR.exists():
        return ""

    nombres = ["theme.css", "report.css"]
    por_pagina = {
        "index": ["panel.css", "explosion.css"],
        "drivers": ["drivers.css"],
        "diagnostico": ["diagnostico.css"],
        "red": ["red.css"],
    }
    nombres += por_pagina.get(pagina, [])
    archivos_css = [CSS_DIR / nombre for nombre in nombres]

    estilos = []

    for archivo in archivos_css:
        estilos.append(
            archivo.read_text(
                encoding="utf-8"
            )
        )

    return "\n\n".join(estilos)


def cargar_js(pagina=None):

    if not JS_DIR.exists():
        return ""

    nombres = ["theme.js"]
    if pagina == "index":
        nombres.append("explosion.js")
    elif pagina == "drivers":
        nombres.append("drivers.js")
    archivos_js = [JS_DIR / nombre for nombre in nombres]

    scripts = []

    for archivo in archivos_js:
        scripts.append(
            archivo.read_text(
                encoding="utf-8"
            )
        )

    return "\n;\n".join(scripts)


def cargar_explosion_random():

    if not EXPLOSIONES_DIR.exists():
        return ""

    gifs = list(
        EXPLOSIONES_DIR.glob("*.gif")
    )

    if not gifs:
        return ""

    gif = random.choice(gifs)

    contenido = base64.b64encode(
        gif.read_bytes()
    ).decode("utf-8")
    
    return (
        "data:image/gif;base64,"
        + contenido
    )

