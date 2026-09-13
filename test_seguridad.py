from modules.seguridad.analisis import (
    analizar_archivo
)

archivo = r"C:\Windows\System32\notepad.exe"

resultado = analizar_archivo(
    archivo
)

print(resultado)