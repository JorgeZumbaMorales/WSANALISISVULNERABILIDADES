import subprocess
import re
from typing import Optional

def detectar_sistema_operativo(ip: str) -> Optional[str]:
    """
    Realiza detección del sistema operativo de un host mediante Nmap.
    Requiere privilegios elevados para ejecutar la detección (-O).
    """
    try:
        comando = ["sudo", "nmap", "-O", ip]
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        salida = resultado.stdout

        match = re.search(r"OS details: (.+)", salida)
        if match:
            return match.group(1).strip()

        # Si no encuentra detalles exactos, intenta con la línea "Running"
        match_running = re.search(r"Running: (.+)", salida)
        if match_running:
            return match_running.group(1).strip()

        return None

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error al detectar el sistema operativo de {ip}: {e}")
        return None
