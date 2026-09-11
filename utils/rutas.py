from pathlib import Path
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent


HTML_DIR = BASE_DIR / "HTML"
DRIVERS_DIR = BASE_DIR / "DRIVERS_EXPORTADOS"

HTML_DIR.mkdir(exist_ok=True)
DRIVERS_DIR.mkdir(exist_ok=True)