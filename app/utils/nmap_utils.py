import subprocess
import shutil
import re
from arp_scan_utils import escanear_red

def verificar_instalacion(comando):
    """Verifica si un comando está instalado en el sistema."""
    return shutil.which(comando) is not None

def escanear_tcp(ip):
    """Escanea los puertos TCP más comunes y el sistema operativo."""
    print(f"🔍 Escaneando TCP en {ip}...")
    resultado = subprocess.run(
        ["sudo", "nmap", "-sS", "--top-ports", "100", "-O", "--osscan-guess", "--max-os-tries", "1", ip],  
        text=True,
        capture_output=True
    )
    return resultado.stdout if resultado.returncode == 0 else None

def escanear_udp(ip):
    """Escanea los puertos UDP más comunes."""
    print(f"🔍 Escaneando UDP en {ip}...")
    resultado = subprocess.run(
        ["sudo", "nmap", "-sU", "--top-ports", "50", ip],  
        text=True,
        capture_output=True
    )
    return resultado.stdout if resultado.returncode == 0 else None

def analizar_salida_nmap(salida):
    """Analiza la salida de Nmap y extrae información relevante."""
    if not salida:
        return [], "No disponible"

    # 🔍 Detectar si hay demasiadas coincidencias en SO
    if "Too many fingerprints match this host" in salida:
        sistemas_operativos = ["Demasiadas coincidencias para determinar un SO específico"]
    else:
        so_match = re.findall(r"Aggressive OS guesses: (.+)", salida)
        sistemas_operativos = so_match[0].split(", ")[:3] if so_match else ["Desconocido"]

    # 🔍 Extraer fingerprint si está disponible
    fingerprint_match = re.search(r"TCP/IP fingerprint:\n(.*)", salida, re.DOTALL)
    fingerprint = fingerprint_match.group(1).strip() if fingerprint_match else "No disponible"

    # 🔍 Extraer puertos abiertos
    puertos_abiertos = []
    for linea in salida.split("\n"):
        puerto_match = re.match(r"(\d+)/(tcp|udp)\s+(open|closed|filtered)\s+(.+)", linea)
        if puerto_match:
            puertos_abiertos.append({
                "puerto": puerto_match.group(1),
                "protocolo": puerto_match.group(2),  # TCP o UDP
                "estado": puerto_match.group(3),
                "servicio": puerto_match.group(4)
            })

    return sistemas_operativos, fingerprint, puertos_abiertos

def escanear_dispositivo(ip, mac):
    """Ejecuta los escaneos de TCP y UDP por separado para optimizar velocidad."""
    if not verificar_instalacion("nmap"):
        print("Error: Nmap no está instalado.")
        return None

    print(f"🚀 Iniciando escaneo de {ip} (MAC: {mac})...")

    # 🔍 Escaneo TCP primero
    salida_tcp = escanear_tcp(ip)
    so_tcp, fingerprint_tcp, puertos_tcp = analizar_salida_nmap(salida_tcp)

    # 🔍 Escaneo UDP después
    salida_udp = escanear_udp(ip)
    _, _, puertos_udp = analizar_salida_nmap(salida_udp)  # Solo nos interesa extraer puertos UDP

    return {
        "ip": ip,
        "mac": mac,
        "sistemas_operativos": so_tcp,
        "fingerprint": fingerprint_tcp,
        "puertos_abiertos": puertos_tcp + puertos_udp  # ✅ Mezclamos TCP y UDP
    }

if __name__ == "__main__":
    dispositivos_activos = escanear_red()
    for dispositivo in dispositivos_activos:
        info_dispositivo = escanear_dispositivo(dispositivo["ip"], dispositivo["mac"])
        if info_dispositivo:
            print(f"📌 Dispositivo {info_dispositivo['ip']} (MAC: {info_dispositivo['mac']}) escaneado:")
            print(f"Sistemas operativos posibles: {', '.join(info_dispositivo['sistemas_operativos'])}")
            print(f"Fingerprint: {info_dispositivo['fingerprint']}")
            print("Puertos abiertos:")
            for puerto in info_dispositivo["puertos_abiertos"]:
                print(f"  - {puerto['puerto']}/{puerto['protocolo']} ({puerto['estado']} - {puerto['servicio']})")
            print()
