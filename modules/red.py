from utils.comandos import ejecutar


def diagnosticar_red():

    resultado = []

    resultado.append("=== CONFIGURACIÓN DE RED ===\n")

    resultado.append(
        ejecutar("ipconfig /all")
    )

    resultado.append(
        "\n\n=== CONECTIVIDAD ===\n"
    )

    resultado.append(
        ejecutar("ping 8.8.8.8 -n 4")
    )

    resultado.append(
        "\n\n=== DNS ===\n"
    )

    resultado.append(
        ejecutar("nslookup google.com")
    )

    return "\n".join(resultado)