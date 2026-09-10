from pathlib import Path
import sys


if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent


REPORTES_DIR = BASE_DIR / "REPORTES"
DRIVERS_DIR = BASE_DIR / "DRIVERS_EXPORTADOS"


REPORTES_DIR.mkdir(exist_ok=True)
DRIVERS_DIR.mkdir(exist_ok=True)