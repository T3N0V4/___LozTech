import json
import subprocess


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


def obtener_antivirus():
    comando = r"""
Get-CimInstance `
    -Namespace root/SecurityCenter2 `
    -ClassName AntivirusProduct |
Select-Object `
    displayName,
    productState,
    pathToSignedProductExe,
    pathToSignedReportingExe |
ConvertTo-Json -Depth 3
"""

    salida = ejecutar_powershell(
        comando
    )

    if not salida:
        return []

    try:
        datos = json.loads(
            salida
        )

    except json.JSONDecodeError:
        return []

    if isinstance(datos, dict):
        datos = [datos]

    resultado = []

    for antivirus in datos:
        resultado.append({
            "nombre": antivirus.get(
                "displayName"
            ),
            "estado_codigo": antivirus.get(
                "productState"
            ),
            "ejecutable": antivirus.get(
                "pathToSignedProductExe"
            ),
            "reporting_exe": antivirus.get(
                "pathToSignedReportingExe"
            )
        })

    return resultado