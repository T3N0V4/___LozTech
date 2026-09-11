import json
import socket

from datetime import datetime

from utils.comandos import ejecutar
from utils.rutas import HTML_DIR
from utils.html_report import crear_reporte_html


# ============================================================
# POWERSHELL -> JSON
# ============================================================

def ejecutar_json(comando):
    powershell = (
        'powershell -NoProfile -Command "'
        '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; '
        f'{comando} '
        '| ConvertTo-Json -Depth 6 -Compress'
        '"'
    )

    resultado = ejecutar(powershell)

    if not resultado or resultado == "Sin información.":
        return None

    try:
        return json.loads(resultado)
    except json.JSONDecodeError:
        return None


def como_lista(valor):
    if valor is None:
        return []

    if isinstance(valor, list):
        return valor

    return [valor]


def bytes_a_gb(valor):
    if not valor:
        return 0

    return valor / (1024 ** 3)


# ============================================================
# INFORMACIÓN GENERAL
# ============================================================

def obtener_equipo():
    datos = ejecutar_json(
        "$pc = Get-CimInstance Win32_ComputerSystem; "
        "$os = Get-CimInstance Win32_OperatingSystem; "
        "[PSCustomObject]@{ "
        "Fabricante = $pc.Manufacturer; "
        "Modelo = $pc.Model; "
        "Windows = $os.Caption; "
        "Build = $os.BuildNumber "
        "}"
    )

    if not datos:
        return {}

    return datos


# ============================================================
# RAM
# ============================================================

def chequear_ram():
    datos = ejecutar_json(
        "$os = Get-CimInstance Win32_OperatingSystem; "
        "$pc = Get-CimInstance Win32_ComputerSystem; "
        "[PSCustomObject]@{ "
        "Total = $pc.TotalPhysicalMemory; "
        "Libre = ($os.FreePhysicalMemory * 1KB) "
        "}"
    )

    if not datos:
        return {
            "titulo": "Memoria RAM",
            "estado": "info",
            "resumen": "No se pudo obtener información.",
            "detalles": ""
        }

    total = bytes_a_gb(datos.get("Total", 0))
    libre = bytes_a_gb(datos.get("Libre", 0))
    usada = max(total - libre, 0)

    porcentaje = 0

    if total > 0:
        porcentaje = (usada / total) * 100

    if porcentaje >= 95:
        estado = "error"
        resumen = f"Uso muy alto: {porcentaje:.0f}%"

    elif porcentaje >= 85:
        estado = "warning"
        resumen = f"Uso elevado: {porcentaje:.0f}%"

    else:
        estado = "ok"
        resumen = f"Uso normal: {porcentaje:.0f}%"

    detalles = (
        f"Instalada: {total:.1f} GB\n"
        f"En uso: {usada:.1f} GB\n"
        f"Libre: {libre:.1f} GB"
    )

    return {
        "titulo": "Memoria RAM",
        "estado": estado,
        "resumen": resumen,
        "detalles": detalles,
        "progreso": round(porcentaje)
    }


# ============================================================
# DISCO DEL SISTEMA
# ============================================================

def chequear_espacio_sistema():
    datos = ejecutar_json(
        "$nombre = $env:SystemDrive.TrimEnd(':'); "
        "$drive = Get-PSDrive -Name $nombre; "
        "[PSCustomObject]@{ "
        "Unidad = $env:SystemDrive; "
        "Usado = $drive.Used; "
        "Libre = $drive.Free "
        "}"
    )

    if not datos:
        return {
            "titulo": "Espacio del sistema",
            "estado": "info",
            "resumen": "No se pudo obtener información.",
            "detalles": ""
        }

    usado = bytes_a_gb(datos.get("Usado", 0))
    libre = bytes_a_gb(datos.get("Libre", 0))

    total = usado + libre

    porcentaje_libre = 0
    porcentaje_usado = 0

    if total > 0:
        porcentaje_libre = (libre / total) * 100
        porcentaje_usado = (usado / total) * 100

    if porcentaje_libre <= 7:
        estado = "error"
        resumen = f"Espacio crítico: {libre:.1f} GB libres"

    elif porcentaje_libre <= 15:
        estado = "warning"
        resumen = f"Poco espacio: {libre:.1f} GB libres"

    else:
        estado = "ok"
        resumen = f"{libre:.1f} GB disponibles"

    return {
        "titulo": f"Disco del sistema ({datos.get('Unidad', 'C:')})",
        "estado": estado,
        "resumen": resumen,
        "detalles": (
            f"Capacidad: {total:.1f} GB\n"
            f"Usado: {usado:.1f} GB\n"
            f"Libre: {libre:.1f} GB"
        ),
        "progreso": round(porcentaje_usado)
    }


# ============================================================
# SALUD DE DISCOS
# ============================================================

def chequear_discos():
    datos = ejecutar_json(
        "Get-PhysicalDisk "
        "| Select-Object "
        "FriendlyName,MediaType,HealthStatus,"
        "OperationalStatus,Size"
    )

    discos = como_lista(datos)

    if not discos:
        return {
            "titulo": "Discos físicos",
            "estado": "info",
            "resumen": "No se pudo consultar el estado.",
            "detalles": ""
        }

    problemas = []
    detalles = []

    for disco in discos:
        nombre = disco.get(
            "FriendlyName",
            "Disco desconocido"
        )

        estado = disco.get(
            "HealthStatus",
            "Unknown"
        )

        tipo = disco.get(
            "MediaType",
            "Desconocido"
        )

        tamaño = bytes_a_gb(
            disco.get("Size", 0)
        )

        detalles.append(
            f"{nombre}\n"
            f"{tipo} · {tamaño:.1f} GB · {estado}"
        )

        if estado.lower() != "healthy":
            problemas.append(
                f"{nombre}: {estado}"
            )

    if problemas:
        estado_general = "error"
        resumen = (
            f"{len(problemas)} disco(s) requieren atención"
        )

    else:
        estado_general = "ok"
        resumen = (
            f"{len(discos)} disco(s), sin alertas"
        )

    return {
        "titulo": "Discos físicos",
        "estado": estado_general,
        "resumen": resumen,
        "detalles": "\n\n".join(detalles)
    }


# ============================================================
# DISPOSITIVOS CON ERROR
# ============================================================

CODIGOS_IMPORTANTES = {
    10: "El dispositivo no puede iniciarse",
    12: "No hay suficientes recursos",
    18: "Es necesario reinstalar el driver",
    22: "El dispositivo está deshabilitado",
    28: "El driver no está instalado",
    31: "Windows no puede cargar el driver",
    37: "Windows no puede inicializar el driver",
    39: "El driver falta o está dañado",
    43: "El dispositivo informó un problema",
    48: "Windows bloqueó el driver",
    52: "No se puede verificar la firma del driver"
}


def chequear_dispositivos():
    codigos = ",".join(
        str(codigo)
        for codigo in CODIGOS_IMPORTANTES
    )

    datos = ejecutar_json(
        "Get-CimInstance Win32_PnPEntity "
        f"| Where-Object {{ $_.ConfigManagerErrorCode -in @({codigos}) }} "
        "| Select-Object "
        "Name,PNPClass,ConfigManagerErrorCode"
    )

    dispositivos = como_lista(datos)

    if not dispositivos:
        return {
            "titulo": "Dispositivos y drivers",
            "estado": "ok",
            "resumen": "No se detectaron problemas importantes.",
            "detalles": ""
        }

    detalles = []

    for dispositivo in dispositivos:
        codigo = dispositivo.get(
            "ConfigManagerErrorCode"
        )

        descripcion = CODIGOS_IMPORTANTES.get(
            codigo,
            "Error desconocido"
        )

        detalles.append(
            f"{dispositivo.get('Name', 'Dispositivo desconocido')}\n"
            f"{descripcion} · Código {codigo}"
        )

    return {
        "titulo": "Dispositivos y drivers",
        "estado": "warning",
        "resumen": (
            f"{len(dispositivos)} dispositivo(s) con problemas"
        ),
        "detalles": "\n\n".join(detalles)
    }


# ============================================================
# EVENTOS CRÍTICOS
# ============================================================

def chequear_eventos():
    datos = ejecutar_json(
        "$eventos = @(Get-WinEvent "
        "-FilterHashtable @{ "
        "LogName='System'; "
        "Level=1; "
        "StartTime=(Get-Date).AddHours(-24) "
        "} -ErrorAction SilentlyContinue); "
        "[PSCustomObject]@{ "
        "Cantidad = $eventos.Count; "
        "Eventos = @($eventos | Select-Object -First 5 "
        "TimeCreated,Id,ProviderName,Message) "
        "}"
    )

    if not datos:
        return {
            "titulo": "Eventos críticos",
            "estado": "info",
            "resumen": "No se pudo consultar el Visor de eventos.",
            "detalles": ""
        }

    cantidad = datos.get(
        "Cantidad",
        0
    )

    if cantidad == 0:
        return {
            "titulo": "Eventos críticos",
            "estado": "ok",
            "resumen": "Ningún evento crítico en las últimas 24 h.",
            "detalles": ""
        }

    eventos = como_lista(
        datos.get("Eventos")
    )

    detalles = []

    for evento in eventos:
        mensaje = str(
            evento.get("Message", "")
        )

        # Evitamos meter una novela entera en el reporte
        if len(mensaje) > 300:
            mensaje = mensaje[:300] + "..."

        detalles.append(
            f"{evento.get('ProviderName', 'Windows')} "
            f"(ID {evento.get('Id', '?')})\n"
            f"{mensaje}"
        )

    return {
        "titulo": "Eventos críticos",
        "estado": "warning",
        "resumen": (
            f"{cantidad} evento(s) crítico(s) en las últimas 24 h"
        ),
        "detalles": "\n\n".join(detalles)
    }


# ============================================================
# ARCHIVO DE PAGINACIÓN
# ============================================================

def chequear_paginacion():
    datos = ejecutar_json(
        "$uso = @(Get-CimInstance Win32_PageFileUsage); "
        "$pc = Get-CimInstance Win32_ComputerSystem; "
        "[PSCustomObject]@{ "
        "Automatico = $pc.AutomaticManagedPagefile; "
        "Cantidad = $uso.Count "
        "}"
    )

    if not datos:
        return {
            "titulo": "Memoria virtual",
            "estado": "info",
            "resumen": "No se pudo consultar.",
            "detalles": ""
        }

    cantidad = datos.get(
        "Cantidad",
        0
    )

    automatico = datos.get(
        "Automatico",
        False
    )

    if cantidad == 0:
        return {
            "titulo": "Memoria virtual",
            "estado": "warning",
            "resumen": "No se detectó archivo de paginación activo.",
            "detalles": (
                "Desactivar la memoria virtual puede causar "
                "problemas cuando se agota la RAM."
            )
        }

    if automatico:
        resumen = "Administrada automáticamente por Windows."
    else:
        resumen = "Configuración manual activa."

    return {
        "titulo": "Memoria virtual",
        "estado": "ok",
        "resumen": resumen,
        "detalles": ""
    }


# ============================================================
# GENERAR CHEQUEO
# ============================================================

def generar_diagnostico():
    nombre_pc = socket.gethostname()
    ahora = datetime.now()

    archivo = HTML_DIR / "diagnostico.html"

    equipo = obtener_equipo()

    chequeos = [
        chequear_ram(),
        chequear_espacio_sistema(),
        chequear_discos(),
        chequear_dispositivos(),
        chequear_eventos(),
        chequear_paginacion()
    ]

    subtitulo = (
        f"{equipo.get('Fabricante', '')} "
        f"{equipo.get('Modelo', '')} · "
        f"{equipo.get('Windows', 'Windows')} · "
        f"{ahora.strftime('%d/%m/%Y %H:%M')}"
    )

    crear_reporte_html(
        titulo="Chequeo rápido del sistema",
        subtitulo=subtitulo,
        secciones=chequeos,
        archivo=archivo
    )

    return archivo