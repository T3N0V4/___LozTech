import json

from html import escape

from utils.comandos import ejecutar
from utils.rutas import (
    DRIVERS_DIR,
    HTML_DIR
)

from utils.assets import (
    cargar_css,
    cargar_js,
    cargar_explosion_random
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


def crear_html_drivers(
    drivers
):
    css = cargar_css()
    js = cargar_js()

    explosion = (
        cargar_explosion_random()
    )

    filas = crear_filas(
        drivers
    )

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
        Drivers
    </title>

    <style>
        {css}
    </style>

</head>

<body>

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
                Drivers
            </h1>

            <p>
                Drivers detectados y exportados
                desde el sistema.
            </p>

        </div>

    </header>


    <main class="container">

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

    </main>


    <footer>
        LozTech USB ·
        Drivers exportados localmente
    </footer>


    <script>
        {js}
    </script>

</body>

</html>
"""

    archivo = (
        HTML_DIR
        / "drivers.html"
    )

    archivo.write_text(
        html,
        encoding="utf-8"
    )

    return archivo


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