from pathlib import Path

from utils.html_report import crear_reporte_html


secciones = [
    {
        "titulo": "Memoria RAM",
        "estado": "ok",
        "resumen": "Uso normal: 42%",
        "detalles": (
            "Instalada: 32 GB\n"
            "En uso: 13.4 GB\n"
            "Libre: 18.6 GB"
        ),
        "progreso": 42
    },

    {
        "titulo": "Disco del sistema",
        "estado": "warning",
        "resumen": "Poco espacio disponible",
        "detalles": (
            "Capacidad: 500 GB\n"
            "Usado: 445 GB\n"
            "Libre: 55 GB"
        ),
        "progreso": 89
    },

    {
        "titulo": "Drivers",
        "estado": "error",
        "resumen": "2 dispositivos con problemas",
        "detalles": (
            "Intel Wireless Adapter\n"
            "Driver no instalado · Código 28\n\n"
            "USB Controller\n"
            "El dispositivo no puede iniciarse · Código 10"
        )
    },

    {
        "titulo": "Eventos críticos",
        "estado": "info",
        "resumen": "Sin eventos críticos recientes",
        "detalles": ""
    },

    {
        "titulo": "Memoria virtual",
        "estado": "ok",
        "resumen": "Administrada automáticamente por Windows",
        "detalles": ""
    },

    {
        "titulo": "Discos físicos",
        "estado": "ok",
        "resumen": "2 discos, sin alertas",
        "detalles": (
            "HIKSEMI WAVE 512GB\n"
            "SSD · Healthy\n\n"
            "TOSHIBA 1TB\n"
            "HDD · Healthy"
        )
    }
]


archivo = Path("test_report.html")


crear_reporte_html(
    titulo="Chequeo rápido del sistema",
    subtitulo="PC-DE-PRUEBA · Windows 11 · 10/09/2026",
    secciones=secciones,
    archivo=archivo
)


print(
    f"Reporte generado: "
    f"{archivo.resolve()}"
)