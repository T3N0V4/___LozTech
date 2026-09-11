import json
from utils.html_base import crear_pagina_html
from html import escape
from utils.comandos import ejecutar
from utils.rutas import (
    DRIVERS_DIR,
    HTML_DIR
)

def ejecutar_json(comando):
    powershell = (
        'powershell -NoProfile -Command "'
        '[Console]::OutputEncoding = '
        '[System.Text.Encoding]::UTF8; '
        f'{comando} '
        '| ConvertTo-Json -Depth 5 -Compress'
        '"'
    )

    resultado = ejecutar(
        powershell
    )

    if (
        not resultado
        or resultado == "Sin información."
    ):
        return []

    try:
        datos = json.loads(
            resultado
        )

        if isinstance(
            datos,
            list
        ):
            return datos

        return [datos]

    except json.JSONDecodeError:
        return []


def obtener_drivers():
    return ejecutar_json(
        "Get-CimInstance Win32_PnPSignedDriver "
        "| Where-Object { "
        "$_.DeviceName -and $_.InfName "
        "} "
        "| Select-Object "
        "DeviceName,"
        "Manufacturer,"
        "DeviceClass,"
        "DriverVersion,"
        "InfName "
        "| Sort-Object DeviceName"
    )


def crear_filas(drivers):
    filas = ""

    for driver in drivers:

        nombre = escape(
            str(
                driver.get(
                    "DeviceName",
                    "-"
                )
            )
        )

        fabricante = escape(
            str(
                driver.get(
                    "Manufacturer",
                    "-"
                )
            )
        )

        clase = escape(
            str(
                driver.get(
                    "DeviceClass",
                    "-"
                )
            )
        )

        version = escape(
            str(
                driver.get(
                    "DriverVersion",
                    "-"
                )
            )
        )

        inf = escape(
            str(
                driver.get(
                    "InfName",
                    "-"
                )
            )
        )

        filas += f"""
        <tr>
            <td>{nombre}</td>
            <td>{fabricante}</td>
            <td>{clase}</td>
            <td>{version}</td>
            <td>{inf}</td>
        </tr>
        """

    return filas


def crear_html_drivers(drivers):

    filas = crear_filas(
        drivers
    )

    contenido = f"""
    <div class="drivers-toolbar">

        <input
            id="driver-search"
            class="driver-search"
            type="search"
            placeholder="Buscar driver..."
        >

    </div>


    <div class="driver-count">

        {len(drivers)}
        drivers detectados

    </div>


    <div class="drivers-wrapper">

        <table
            class="drivers-table"
            id="drivers-table"
        >

            <thead>

                <tr>
                    <th>Dispositivo</th>
                    <th>Fabricante</th>
                    <th>Clase</th>
                    <th>Versión</th>
                    <th>INF</th>
                </tr>

            </thead>

            <tbody>
                {filas}
            </tbody>

        </table>

    </div>
    """

    archivo = (
        HTML_DIR
        / "drivers.html"
    )

    return crear_pagina_html(
        titulo="Drivers",
        subtitulo=(
            "Drivers detectados y "
            "exportados desde el sistema."
        ),
        contenido=contenido,
        archivo=archivo,
        footer=(
            "LozTech USB · "
            "Drivers exportados localmente"
        )
    )


def exportar_drivers():

    comando = (
        f'pnputil /export-driver * '
        f'"{DRIVERS_DIR}"'
    )

    ejecutar(
        comando
    )

    drivers = obtener_drivers()

    return crear_html_drivers(
        drivers
    )