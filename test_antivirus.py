from pprint import pprint

from modules.seguridad.antivirus import (
    obtener_antivirus
)

from modules.seguridad.defender import (
    obtener_informacion_defender
)

print("\n=== ANTIVIRUS ===\n")

pprint(
    obtener_antivirus()
)


print("\n=== DEFENDER ===\n")

pprint(
    obtener_informacion_defender()
)