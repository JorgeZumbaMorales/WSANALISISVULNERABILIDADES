from typing import List
import subprocess
import re

def escanear_hosts_activos(rango_red: str) -> List[str]:
    """
    Escanea una red específica y retorna una lista de IPs activas.
    """
    print(f"[INFO] Escaneando hosts activos en {rango_red}...")
    try:
        resultado = subprocess.run(
            ["nmap", "-sn", rango_red],
            capture_output=True,
            text=True,
            check=True
        )
        salida = resultado.stdout

        # 🔍 Mostrar la salida completa del comando Nmap
        print("[DEBUG] Salida completa de Nmap:")
        print(salida)

        ips_encontradas = re.findall(r"Nmap scan report for (?:.+\()?(\d+\.\d+\.\d+\.\d+)\)?", salida)


        print(f"[INFO] {len(ips_encontradas)} host(s) activo(s) detectado(s).")
        return ips_encontradas

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error ejecutando nmap: {e}")
        return []
