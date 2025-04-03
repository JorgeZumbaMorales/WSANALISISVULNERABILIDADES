import subprocess
import re
from typing import List, Dict


def buscar_vulnerabilidades(ip: str, puertos: List[dict]) -> List[Dict[str, any]]:
    print(f"[INFO] Escaneando vulnerabilidades en {ip}...")

    try:
        if not puertos:
            return []
        
        puertos_str = ",".join(str(p["puerto"]) for p in puertos)
        comando = ["nmap", "-sV", "--script", "vulners", "-p", puertos_str, ip]

        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        salida = resultado.stdout

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error al ejecutar el escaneo de vulnerabilidades: {e}")
        return []

    vulnerabilidades = []
    bloque_actual = None

    for linea in salida.splitlines():
        # Nuevo bloque de puerto
        if re.match(r"^\d+/tcp", linea):
            if bloque_actual:
                vulnerabilidades.append(bloque_actual)
            puerto = linea.split("/")[0]
            bloque_actual = {"puerto": puerto, "vulnerabilidades": []}

        # Detectar líneas con CVE/ID + Score + URL (posiblemente con *EXPLOIT*)
        elif re.match(r"^\|?\s*([A-Z0-9\-]+)\s+(\d\.\d)\s+https?://[^\s]+", linea):
            partes = linea.strip("| ").split()
            if len(partes) >= 3:
                vuln_id = partes[0]
                score = float(partes[1])
                url = partes[2]
                exploit = "*EXPLOIT*" in linea.upper()
                bloque_actual["vulnerabilidades"].append({
                    "id": vuln_id,
                    "score": score,
                    "url": url,
                    "exploit": exploit
                })

        # Detectar si hay texto "VULNERABLE"
        elif "VULNERABLE" in linea.upper():
            bloque_actual.setdefault("vulnerabilidades", []).append({
                "id": "VULNERABLE",
                "score": None,
                "url": None,
                "exploit": False,
                "detalle": linea.strip()
            })

    # Agregar último bloque si existe
    if bloque_actual:
        vulnerabilidades.append(bloque_actual)

    print(f"[INFO] Vulnerabilidades encontradas en {ip}: {len(vulnerabilidades)} servicios con hallazgos")
    return vulnerabilidades
