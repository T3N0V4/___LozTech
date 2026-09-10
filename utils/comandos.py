import subprocess


def ejecutar(comando):
    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            shell=True,
            encoding="utf-8",
            errors="replace"
        )

        if resultado.stdout:
            return resultado.stdout.strip()

        if resultado.stderr:
            return resultado.stderr.strip()

        return "Sin información."

    except Exception as error:
        return f"Error ejecutando comando: {error}"