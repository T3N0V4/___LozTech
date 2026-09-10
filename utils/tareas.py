import threading

def ejecutar_tarea(funcion, al_terminar=None, al_fallar=None):
    def tarea():
        try:
            resultado = funcion()

            if al_terminar:
                al_terminar(resultado)

        except Exception as error:
            if al_fallar:
                al_fallar(error)

    hilo = threading.Thread(
        target=tarea,
        daemon=True
    )

    hilo.start()