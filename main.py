import tkinter as tk
import os
from tkinter import ttk, messagebox

from modules.diagnostico import generar_diagnostico
from modules.red import diagnosticar_red
from modules.drivers import exportar_drivers
from utils.rutas import HTML_DIR
from utils.tareas import ejecutar_tarea


def bloquear_interfaz(mensaje):
    estado.config(text=mensaje)
    progreso.start(10)

    for boton in botones:
        boton.config(state="disabled")


def desbloquear_interfaz():
    progreso.stop()
    estado.config(text="Listo")

    for boton in botones:
        boton.config(state="normal")


def manejar_error(error):
    desbloquear_interfaz()

    messagebox.showerror(
        "Error",
        str(error)
    )


def diagnostico():
    bloquear_interfaz(
        "Chequeando el sistema..."
    )

    ejecutar_tarea(
        generar_diagnostico,
        lambda archivo: root.after(
            0,
            diagnostico_terminado,
            archivo
        ),
        lambda error: root.after(
            0,
            manejar_error,
            error
        )
    )


def diagnostico_terminado(archivo):
    desbloquear_interfaz()

    os.startfile(archivo)


def red():
    bloquear_interfaz("Analizando red...")

    ejecutar_tarea(
        diagnosticar_red,
        lambda resultado: root.after(
            0,
            red_terminada,
            resultado
        ),
        lambda error: root.after(
            0,
            manejar_error,
            error
        )
    )


def red_terminada(resultado):
    desbloquear_interfaz()

    ventana = tk.Toplevel(root)
    ventana.title("Diagnóstico de red")
    ventana.geometry("700x500")

    texto = tk.Text(
        ventana,
        wrap="word"
    )

    texto.pack(
        expand=True,
        fill="both"
    )

    texto.insert(
        "1.0",
        resultado
    )

    texto.config(
        state="disabled"
    )


def drivers():
    bloquear_interfaz("Exportando drivers...")

    ejecutar_tarea(
        exportar_drivers,
        lambda resultado: root.after(
            0,
            drivers_terminados,
            resultado
        ),
        lambda error: root.after(
            0,
            manejar_error,
            error
        )
    )


def drivers_terminados(archivo):
    desbloquear_interfaz()

    os.startfile(archivo)


def abrir_reportes():
    archivo = HTML_DIR / "diagnostico.html"

    if archivo.exists():
        os.startfile(archivo)
    else:
        os.startfile(HTML_DIR)


root = tk.Tk()

root.title("LozTech USB")
root.geometry("420x430")
root.resizable(False, False)


titulo = tk.Label(
    root,
    text="LOZ TECH USB",
    font=("Segoe UI", 20, "bold")
)

titulo.pack(
    pady=25
)


botones = []


def crear_boton(texto, comando):
    boton = tk.Button(
        root,
        text=texto,
        width=30,
        height=2,
        command=comando
    )

    boton.pack(
        pady=5
    )

    botones.append(
        boton
    )

    return boton


crear_boton(
    "Chequear sistema",
    diagnostico
)

crear_boton(
    "Diagnóstico de red",
    red
)

crear_boton(
    "Exportar drivers",
    drivers
)

crear_boton(
    "Abrir panel",
    abrir_reportes
)


estado = tk.Label(
    root,
    text="Listo",
    font=("Segoe UI", 10)
)

estado.pack(
    pady=(20, 5)
)


progreso = ttk.Progressbar(
    root,
    mode="indeterminate",
    length=280
)

progreso.pack()


root.mainloop()