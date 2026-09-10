import base64
import random

from utils.rutas import BASE_DIR


CSS_FILE = (
    BASE_DIR
    / "assets"
    / "css"
    / "report.css"
)

JS_FILE = (
    BASE_DIR
    / "assets"
    / "js"
    / "explosion.js"
)

EXPLOSIONES_DIR = (
    BASE_DIR
    / "assets"
    / "explosiones"
)


def cargar_css():
    if not CSS_FILE.exists():
        return ""

    return CSS_FILE.read_text(
        encoding="utf-8"
    )


def cargar_js():
    if not JS_FILE.exists():
        return ""

    return JS_FILE.read_text(
        encoding="utf-8"
    )


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