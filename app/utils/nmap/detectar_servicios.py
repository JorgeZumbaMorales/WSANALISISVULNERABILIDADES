import subprocess
import re
from typing import List, Dict

def detectar_servicios(ip: str, puertos: List[int]) -> List[Dict[str, str]]:
    """
    Ejecuta un escaneo Nmap en los puertos especificados para detectar servicios y versiones.
    Retorna una lista de diccionarios con los detalles de cada puerto.
    """
    if not puertos:
        return []

    puertos_str = ",".join(str(p["puerto"]) for p in puertos)

    comando = ["nmap", "-sV", "-p", puertos_str, ip]


    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        salida = resultado.stdout

        servicios_detectados = []
        for linea in salida.splitlines():
            match = re.match(r"(\d+)/tcp\s+open\s+(\S+)(\s+.+)?", linea)
            if match:
                puerto, servicio, version = match.groups()
                servicios_detectados.append({
                    "puerto": puerto,
                    "servicio": servicio,
                    "version": version.strip() if version else "No disponible"
                })

        return servicios_detectados

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error al detectar servicios en {ip}: {e}")
        return []
