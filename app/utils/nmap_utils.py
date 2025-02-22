import subprocess
import shutil
import re
from arp_scan_utils import escanear_red

def verificar_instalacion(comando):
    """Verifica si un comando está instalado en el sistema."""
    return shutil.which(comando) is not None

def escanear_dispositivo(ip):
    """Escanea un dispositivo con Nmap para obtener información detallada."""
    if not verificar_instalacion("nmap"):
        print("Error: Nmap no está instalado. Instálalo con 'sudo apt install nmap' en Linux.")
        return None
    
    try:
        print(f"🔍 Escaneando {ip} con Nmap...")
        resultado = subprocess.run(
            ["sudo", "nmap", "-O", "-sV", "--osscan-guess", ip],  # Se ejecuta con sudo para permisos elevados y mejora la detección
            text=True,
            capture_output=True
        )
        if resultado.returncode != 0:
            print(f"Error ejecutando Nmap: {resultado.stderr}")
            return None

        # Procesar la salida de Nmap
        salida = resultado.stdout
        so_match = re.search(r"OS details: (.+)", salida)
        fingerprint_match = re.search(r"TCP/IP fingerprint:.*?\n(.*)\n", salida, re.DOTALL)
        sistema_operativo = so_match.group(1) if so_match else "Desconocido"
        fingerprint = fingerprint_match.group(1).strip() if fingerprint_match else "No disponible"

        puertos_abiertos = []
        for linea in salida.split("\n"):
            puerto_match = re.match(r"(\d+)/tcp\s+(\w+)\s+(.+)", linea)
            if puerto_match:
                puertos_abiertos.append({
                    "puerto": puerto_match.group(1),
                    "estado": puerto_match.group(2),
                    "servicio": puerto_match.group(3)
                })

        return {
            "ip": ip,
            "sistema_operativo": sistema_operativo,
            "fingerprint": fingerprint,
            "puertos_abiertos": puertos_abiertos
        }
    
    except Exception as e:
        print(f"Error escaneando {ip}: {e}")
        return None

if __name__ == "__main__":
    dispositivos_activos = escanear_red()
    for dispositivo in dispositivos_activos:
        print(f"\n🔍 Escaneando {dispositivo['ip']} ({dispositivo['mac']})...")
        resultado = escanear_dispositivo(dispositivo['ip'])
        if resultado:
            print(f"📌 IP: {resultado['ip']}")
            print(f"🖥️  SO Detectado: {resultado['sistema_operativo']}")
            print(f"🔍 Fingerprint TCP/IP: {resultado['fingerprint']}")
            print("🔓 Puertos abiertos:")
            for puerto in resultado["puertos_abiertos"]:
                print(f"   - {puerto['puerto']}: {puerto['estado']} ({puerto['servicio']})")
