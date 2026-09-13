import json
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
        return None

    salida = resultado.stdout.strip()

    if not salida:
        return None

    return salida


def ejecutar_powershell_json(comando):
    salida = ejecutar_powershell(
        comando
    )

    if not salida:
        return None

    try:
        return json.loads(
            salida
        )

    except json.JSONDecodeError:
        return None


def asegurar_lista(datos):
    if not datos:
        return []

    if isinstance(datos, dict):
        return [datos]

    return datos


def buscar_instalacion_avg():
    program_files = Path(
        os.environ.get(
            "ProgramFiles",
            r"C:\Program Files"
        )
    )

    rutas = [
        program_files / "AVG" / "Antivirus",
        program_files / "AVG"
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

    return ejecutar_powershell_json(
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

    return ejecutar_powershell_json(
        comando
    )


def obtener_version_avg():
    comando = r"""
$paths = @(
    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*"
)

Get-ItemProperty $paths |
Where-Object {
    $_.DisplayName -match '^AVG'
} |
Select-Object `
    DisplayName,
    DisplayVersion,
    Publisher,
    InstallLocation |
ConvertTo-Json -Depth 3
"""

    return ejecutar_powershell_json(
        comando
    )


def obtener_informacion_avg():
    return {
        "rutas_instalacion":
            buscar_instalacion_avg(),

        "servicios":
            asegurar_lista(
                obtener_servicios_avg()
            ),

        "procesos":
            asegurar_lista(
                obtener_procesos_avg()
            ),

        "version":
            asegurar_lista(
                obtener_version_avg()
            )
    }