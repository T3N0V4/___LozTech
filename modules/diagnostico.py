import socket

from datetime import datetime

from utils.comandos import ejecutar
from utils.rutas import REPORTES_DIR
from utils.html_report import crear_reporte_html


def generar_diagnostico():

    nombre_pc = socket.gethostname()

    ahora = datetime.now()

    fecha_archivo = ahora.strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    archivo = (
        REPORTES_DIR
        / f"{nombre_pc}_{fecha_archivo}.html"
    )

    secciones = []


    # WINDOWS

    windows = ejecutar(
        'powershell "'
        'Get-CimInstance Win32_OperatingSystem '
        '| Select-Object Caption,Version,OSArchitecture '
        '| Format-List'
        '"'
    )

    secciones.append({
        "titulo": "Windows",
        "contenido": windows
    })


    # EQUIPO

    equipo = ejecutar(
        'powershell "'
        'Get-CimInstance Win32_ComputerSystem '
        '| Select-Object Manufacturer,Model '
        '| Format-List'
        '"'
    )

    secciones.append({
        "titulo": "Equipo",
        "contenido": equipo
    })


    # CPU

    cpu = ejecutar(
        'powershell "'
        'Get-CimInstance Win32_Processor '
        '| Select-Object '
        'Name,NumberOfCores,NumberOfLogicalProcessors '
        '| Format-List'
        '"'
    )

    secciones.append({
        "titulo": "Procesador",
        "contenido": cpu
    })


    # RAM

    ram = ejecutar(
        'powershell "'
        '$os = Get-CimInstance Win32_OperatingSystem; '
        '$cs = Get-CimInstance Win32_ComputerSystem; '
        '$total = [math]::Round('
        '$cs.TotalPhysicalMemory / 1GB, 2); '
        '$libre = [math]::Round('
        '$os.FreePhysicalMemory / 1MB, 2); '
        '$usada = [math]::Round('
        '$total - $libre, 2); '
        '$porcentaje = [math]::Round('
        '($usada / $total) * 100, 1); '
        'Write-Output \\"RAM instalada: $total GB\\"; '
        'Write-Output \\"RAM usada: $usada GB\\"; '
        'Write-Output \\"RAM libre: $libre GB\\"; '
        'Write-Output \\"Uso: $porcentaje %\\"'
        '"'
    )

    secciones.append({
        "titulo": "Memoria RAM",
        "contenido": ram
    })


    # GPU

    gpu = ejecutar(
        'powershell "'
        'Get-CimInstance Win32_VideoController '
        '| Select-Object Name,DriverVersion '
        '| Format-List'
        '"'
    )

    secciones.append({
        "titulo": "GPU",
        "contenido": gpu
    })


    # DISCOS

    discos = ejecutar(
        'powershell "'
        'Get-PhysicalDisk '
        '| ForEach-Object { '
        '$size = [math]::Round($_.Size / 1GB, 2); '
        'Write-Output \\"$($_.FriendlyName)\\"; '
        'Write-Output \\"Tipo: $($_.MediaType)\\"; '
        'Write-Output \\"Capacidad: $size GB\\"; '
        'Write-Output \\"Estado: $($_.HealthStatus)\\"; '
        'Write-Output \\"\\" '
        '}'
        '"'
    )

    secciones.append({
        "titulo": "Discos físicos",
        "contenido": discos
    })


    # VOLUMENES

    volumenes = ejecutar(
        'powershell "'
        'Get-Volume '
        '| Where-Object {$_.DriveLetter} '
        '| ForEach-Object { '
        '$size = [math]::Round($_.Size / 1GB, 2); '
        '$free = [math]::Round('
        '$_.SizeRemaining / 1GB, 2); '
        'Write-Output '
        '\\"Unidad $($_.DriveLetter):\\"; '
        'Write-Output '
        '\\"Sistema: $($_.FileSystem)\\"; '
        'Write-Output '
        '\\"Capacidad: $size GB\\"; '
        'Write-Output '
        '\\"Libre: $free GB\\"; '
        'Write-Output '
        '\\"Estado: $($_.HealthStatus)\\"; '
        'Write-Output \\"\\" '
        '}'
        '"'
    )

    secciones.append({
        "titulo": "Unidades",
        "contenido": volumenes
    })


    # BIOS

    bios = ejecutar(
        'powershell "'
        'Get-CimInstance Win32_BIOS '
        '| Select-Object '
        'Manufacturer,SMBIOSBIOSVersion,ReleaseDate '
        '| Format-List'
        '"'
    )

    secciones.append({
        "titulo": "BIOS / UEFI",
        "contenido": bios
    })


    # DISPOSITIVOS CON PROBLEMAS

    problemas = ejecutar(
    'powershell "'
    '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; '
    '$problemas = Get-CimInstance Win32_PnPEntity '
    '| Where-Object { $_.ConfigManagerErrorCode -ne 0 }; '
    'if ($problemas) { '
    '$problemas '
    '| Select-Object '
    'Name, '
    'PNPClass, '
    'ConfigManagerErrorCode '
    '| Format-Table -AutoSize '
    '} else { '
    'Write-Output \\"No se detectaron dispositivos con problemas.\\" '
    '}'
    '"'
)

    secciones.append({
        "titulo": "Dispositivos con problemas",
        "contenido": problemas
    })


    subtitulo = (
        f"Equipo: {nombre_pc} | "
        f"{ahora.strftime('%d/%m/%Y %H:%M:%S')}"
    )


    crear_reporte_html(
        titulo="LozTech - Diagnóstico del equipo",
        subtitulo=subtitulo,
        secciones=secciones,
        archivo=archivo
    )

    return archivo