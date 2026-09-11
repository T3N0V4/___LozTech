import subprocess


def decodificar(texto):

    if not texto:
        return ""

    codificaciones = [
        "utf-8",
        "cp850",
        "cp1252"
    ]

    for codificacion in codificaciones:

        try:
            return texto.decode(
                codificacion
            )

        except UnicodeDecodeError:
            continue

    return texto.decode(
        "utf-8",
        errors="replace"
    )


def ejecutar(comando):

    try:

        resultado = subprocess.run(
            comando,
            capture_output=True,
            shell=True
        )

        salida = decodificar(
            resultado.stdout
        ).strip()

        error = decodificar(
            resultado.stderr
        ).strip()

        if salida:
            return salida

        if error:
            return error

        return "Sin información."

    except Exception as error:

        return (
            "Error ejecutando comando: "
            f"{error}"
        )