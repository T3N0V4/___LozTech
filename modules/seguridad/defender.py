import json
import subprocess


def ejecutar_powershell_json(comando):
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

    try:
        return json.loads(
            salida
        )

    except json.JSONDecodeError:
        return None


def obtener_estado_defender():
    comando = r"""
Get-MpComputerStatus |
Select-Object `
    AntivirusEnabled,
    AntispywareEnabled,
    AMServiceEnabled,
    RealTimeProtectionEnabled,
    BehaviorMonitorEnabled,
    IoavProtectionEnabled,
    NISEnabled,
    OnAccessProtectionEnabled,
    AntivirusSignatureVersion,
    AntivirusSignatureLastUpdated,
    AMEngineVersion,
    AMProductVersion |
ConvertTo-Json
"""

    return ejecutar_powershell_json(
        comando
    )


def obtener_exclusiones_defender():
    comando = r"""
Get-MpPreference |
Select-Object `
    ExclusionPath,
    ExclusionProcess,
    ExclusionExtension,
    ExclusionIpAddress |
ConvertTo-Json -Depth 4
"""

    datos = ejecutar_powershell_json(
        comando
    )

    if not datos:
        return {
            "rutas": [],
            "procesos": [],
            "extensiones": [],
            "ips": []
        }

    return {
        "rutas": (
            datos.get(
                "ExclusionPath"
            )
            or []
        ),
        "procesos": (
            datos.get(
                "ExclusionProcess"
            )
            or []
        ),
        "extensiones": (
            datos.get(
                "ExclusionExtension"
            )
            or []
        ),
        "ips": (
            datos.get(
                "ExclusionIpAddress"
            )
            or []
        )
    }


def obtener_detecciones_defender():
    comando = r"""
Get-MpThreatDetection |
Select-Object `
    InitialDetectionTime,
    LastThreatStatusChangeTime,
    ThreatID,
    ThreatStatusID,
    ActionSuccess,
    CurrentThreatExecutionStatusID,
    Resources |
Sort-Object InitialDetectionTime -Descending |
ConvertTo-Json -Depth 5
"""

    datos = ejecutar_powershell_json(
        comando
    )

    if not datos:
        return []

    if isinstance(
        datos,
        dict
    ):
        datos = [datos]

    return datos


def obtener_amenazas_defender():
    comando = r"""
Get-MpThreat |
Select-Object `
    ThreatID,
    ThreatName,
    SeverityID,
    CategoryID,
    DidThreatExecute,
    IsActive |
ConvertTo-Json -Depth 4
"""

    datos = ejecutar_powershell_json(
        comando
    )

    if not datos:
        return []

    if isinstance(
        datos,
        dict
    ):
        datos = [datos]

    return datos


def obtener_informacion_defender():
    return {
        "estado":
            obtener_estado_defender(),

        "exclusiones":
            obtener_exclusiones_defender(),

        "amenazas":
            obtener_amenazas_defender(),

        "detecciones":
            obtener_detecciones_defender()
    }