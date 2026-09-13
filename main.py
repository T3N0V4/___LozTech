import tkinter as tk
import os
from tkinter import ttk, messagebox
from utils.html_index import crear_index
from modules.diagnostico import generar_diagnostico
from modules.red import diagnosticar_red
from modules.drivers import exportar_drivers
from utils.rutas import HTML_DIR
from utils.tareas import ejecutar_tarea
from tkinter import filedialog

from modules.seguridad import analizar_archivo
from utils.html_seguridad import crear_html_seguridad

def bloquear_interfaz(mensaje):
    estado.config(text=mensaje, fg=COLORES["info"])
    progreso.start(10)

    for boton in botones:
        boton.config(state="disabled")


def desbloquear_interfaz(mensaje="Listo para trabajar"):
    progreso.stop()
    estado.config(text=mensaje, fg=COLORES["ok"])

    for boton in botones:
        boton.config(state="normal")


def manejar_error(error):
    desbloquear_interfaz("No se pudo completar la acción.")
    estado.config(fg=COLORES["error"])

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
    desbloquear_interfaz("Diagnóstico listo. Consultalo en «Abrir panel».")


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

def red_terminada(archivo):
    desbloquear_interfaz("Análisis de red listo. Consultalo en «Abrir panel».")


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
    desbloquear_interfaz("Drivers exportados. Consultalos en «Abrir panel».")

def abrir_reportes():
    try:
        archivo = crear_index()
        os.startfile(archivo)
    except Exception as error:
        manejar_error(error)

def seguridad():

    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo para analizar"
    )

    if not archivo:
        return

    bloquear_interfaz(
        "Analizando archivo..."
    )

    ejecutar_tarea(
        lambda: analizar_archivo(
            archivo
        ),
        lambda resultado: root.after(
            0,
            seguridad_terminada,
            resultado
        ),
        lambda error: root.after(
            0,
            manejar_error,
            error
        )
    )

def seguridad_terminada(resultado):
    try:
        crear_html_seguridad(resultado)
    except Exception as error:
        manejar_error(error)
        return

    desbloquear_interfaz("Análisis de archivo listo. Consultalo en «Abrir panel».")


# Misma paleta y tipografía que el tema Black de la web.
COLORES = {
    "fondo": "#0d0f12",
    "superficie": "#15181d",
    "hover": "#20303e",
    "texto": "#edf0f3",
    "secundario": "#adb6c2",
    "borde": "#2a3038",
    "info": "#7b9bb8",
    "ok": "#43c590",
    "error": "#e56363",
}

root = tk.Tk()

root.title("LozTech USB")
root.geometry("520x660")
root.minsize(480, 640)
root.configure(bg=COLORES["fondo"])

estilo = ttk.Style(root)
estilo.theme_use("clam")
estilo.configure(
    "Herramienta.TButton",
    font=("Segoe UI", 11),
    padding=(16, 12),
    anchor="w",
    background=COLORES["superficie"],
    foreground=COLORES["texto"],
    bordercolor=COLORES["borde"],
    lightcolor=COLORES["borde"],
    darkcolor=COLORES["borde"],
    focuscolor=COLORES["info"],
)
estilo.map(
    "Herramienta.TButton",
    background=[("disabled", COLORES["superficie"]), ("active", COLORES["hover"])],
    foreground=[("disabled", COLORES["secundario"])],
    bordercolor=[("focus", COLORES["info"])],
)
estilo.configure(
    "Panel.Herramienta.TButton",
    font=("Segoe UI", 11, "bold"),
    anchor="center",
    background=COLORES["info"],
    foreground=COLORES["fondo"],
    focuscolor=COLORES["fondo"],
)
estilo.map(
    "Panel.Herramienta.TButton",
    background=[("disabled", COLORES["borde"]), ("active", "#9ab5ce")],
    foreground=[("disabled", COLORES["secundario"]), ("!disabled", COLORES["fondo"])],
)
estilo.configure(
    "LozTech.Horizontal.TProgressbar",
    background=COLORES["info"],
    troughcolor=COLORES["borde"],
    bordercolor=COLORES["borde"],
    lightcolor=COLORES["info"],
    darkcolor=COLORES["info"],
    borderwidth=0,
    thickness=5,
)

contenido = tk.Frame(root, bg=COLORES["fondo"], padx=24, pady=22)
contenido.pack(fill="both", expand=True)

tk.Label(
    contenido, text="LOZTECH  /  USB", font=("Segoe UI", 11, "bold"),
    bg=COLORES["fondo"], fg=COLORES["info"],
).pack(anchor="w")


titulo = tk.Label(
    contenido,
    text="Herramientas",
    font=("Segoe UI", 24, "bold"),
    bg=COLORES["fondo"],
    fg=COLORES["texto"],
)

titulo.pack(anchor="w", pady=(10, 4))

tk.Label(
    contenido,
    text="Ejecutá una tarea y consultá sus resultados en el panel.",
    font=("Segoe UI", 10), justify="left", wraplength=420,
    bg=COLORES["fondo"], fg=COLORES["secundario"],
).pack(anchor="w")

acciones = tk.Frame(contenido, bg=COLORES["fondo"])
acciones.pack(fill="x", pady=(18, 12))


botones = []


def crear_boton(texto, comando, principal=False):
    boton = ttk.Button(
        contenido if principal else acciones,
        text=texto,
        command=comando,
        style="Panel.Herramienta.TButton" if principal else "Herramienta.TButton",
        takefocus=True,
    )

    boton.pack(fill="x", pady=4)
    boton.bind("<Return>", lambda event: boton.invoke())

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
    "Analizar archivo",
    seguridad
)

crear_boton(
    "Abrir panel",
    abrir_reportes,
    principal=True,
)

tk.Label(
    contenido, text="Todos tus reportes, en un solo lugar.",
    font=("Segoe UI", 9), bg=COLORES["fondo"], fg=COLORES["secundario"],
).pack(pady=(4, 0))

estado = tk.Label(
    contenido,
    text="Listo para trabajar",
    font=("Segoe UI", 10),
    bg=COLORES["fondo"],
    fg=COLORES["ok"],
    wraplength=420,
    justify="left",
    anchor="w",
)

estado.pack(
    fill="x", pady=(18, 8)
)


barra = tk.Frame(contenido, height=6, bg=COLORES["borde"])
barra.pack(fill="x")
barra.pack_propagate(False)

progreso = ttk.Progressbar(
    barra,
    mode="indeterminate",
    style="LozTech.Horizontal.TProgressbar",
    takefocus=False,
)

progreso.pack(fill="both", expand=True)


root.mainloop()
