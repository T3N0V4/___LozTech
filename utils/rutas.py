from pathlib import Path
import sys


if getattr(sys, "frozen", False):

    # Carpeta donde está LozTech.exe
    APP_DIR = Path(
        sys.executable
    ).parent

    # Recursos empaquetados por PyInstaller
    RESOURCE_DIR = Path(
        sys._MEIPASS
    )

else:

    # Desarrollo normal con Python
    APP_DIR = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

    RESOURCE_DIR = APP_DIR


HTML_DIR = (
    APP_DIR
    / "HTML"
)

DRIVERS_DIR = (
    APP_DIR
    / "DRIVERS_EXPORTADOS"
)


HTML_DIR.mkdir(
    exist_ok=True
)

DRIVERS_DIR.mkdir(
    exist_ok=True
)