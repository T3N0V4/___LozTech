import os
import subprocess
from pathlib import Path


def ejecutar_powershell(comando):
    resultado = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            comando
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if resultado.returncode != 0:
        return ""

    return resultado.stdout.strip()


def buscar_instalacion_avg():
    rutas = [
        Path(
            os.environ.get(
                "ProgramFiles",
                r"C:\Program Files"
            )
        ) / "AVG" / "Antivirus",

        Path(
            os.environ.get(
                "ProgramFiles",
                r"C:\Program Files"
            )
        ) / "AVG"
    ]

    encontradas = []

    for ruta in rutas:
        if ruta.exists():
            encontradas.append(
                str(ruta)
            )

    return encontradas


def obtener_servicios_avg():
    comando = r"""
Get-Service |
Where-Object {
    $_.Name -match 'AVG' -or
    $_.DisplayName -match 'AVG'
} |
Select-Object `
    Name,
    DisplayName,
    Status,
    StartType |
ConvertTo-Json -Depth 3
"""

    return ejecutar_powershell(
        comando
    )


def obtener_procesos_avg():
    comando = r"""
Get-Process |
Where-Object {
    $_.ProcessName -match 'avg'
} |
Select-Object `
    ProcessName,
    Id,
    Path |
ConvertTo-Json -Depth 3
"""

    return ejecutar_powershell(
        comando
    )


def obtener_version_avg():
    comando = r"""
Get-CimInstance Win32_Product |
Where-Object {
    $_.Name -match '^AVG'
} |
Select-Object `
    Name,
    Version,
    Vendor |
ConvertTo-Json -Depth 3
"""

    return ejecutar_powershell(
        comando
    )


def obtener_informacion_avg():
    return {
        "rutas_instalacion":
            buscar_instalacion_avg(),

        "servicios":
            obtener_servicios_avg(),

        "procesos":
            obtener_procesos_avg(),

        "version":
            obtener_version_avg()
    }