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


def cargar_css():

    if not CSS_DIR.exists():
        return ""

    archivos_css = sorted(
        CSS_DIR.glob("*.css")
    )

    estilos = []

    for archivo in archivos_css:
        estilos.append(
            archivo.read_text(
                encoding="utf-8"
            )
        )

    return "\n\n".join(estilos)


def cargar_js():

    if not JS_DIR.exists():
        return ""

    archivos_js = sorted(
        JS_DIR.glob("*.js")
    )

    scripts = []

    for archivo in archivos_js:
        scripts.append(
            archivo.read_text(
                encoding="utf-8"
            )
        )

    return "\n\n".join(scripts)


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

