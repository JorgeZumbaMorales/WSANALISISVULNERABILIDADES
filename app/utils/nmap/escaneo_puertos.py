import subprocess
import re
from typing import List, Dict

def escanear_puertos(ip: str) -> List[Dict]:
    """
    Escanea todos los puertos TCP de la IP especificada y retorna una lista de puertos abiertos con información básica.
    """
    print(f"[INFO] Escaneando puertos abiertos en {ip}...")

    comando = [
        "nmap",
        "-p-",           # Todos los puertos
        "--min-rate", "5000",
        "--open",        # Solo mostrar los abiertos
        "-T4",           # Aumenta la velocidad de escaneo
        ip
    ]

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        salida = resultado.stdout

        puertos_abiertos = []
        for linea in salida.splitlines():
            match = re.match(r"(\d+)/tcp\s+open", linea)
            if match:
                puertos_abiertos.append({
                    "puerto": int(match.group(1)),
                    "protocolo": "tcp"
                })

        print(f"[INFO] Puertos abiertos encontrados en {ip}: {len(puertos_abiertos)}")
        return puertos_abiertos

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Fallo al escanear puertos en {ip}: {e}")
        return []
