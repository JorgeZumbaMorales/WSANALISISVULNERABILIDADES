import subprocess
import shutil
import re
import requests
import json
from scapy_utils import procesar_y_guardar_nmap  

NMAP_DB_PATH = "datos/nmap-os-db"  # Ruta relativa dentro de tu proyecto


def verificar_instalacion(comando):
    """Verifica si un comando está instalado en el sistema."""
    return shutil.which(comando) is not None

def obtener_fabricante(mac):
    """Obtiene el fabricante del dispositivo usando una API externa."""
    try:
        url = f"https://api.macvendors.com/{mac}"
        response = requests.get(url)
        return response.text if response.status_code == 200 else "Desconocido"
    except:
        return "Desconocido"

def escanear_tcp(ip):
    """Escanea los puertos TCP más comunes, detectando servicios y versiones."""
    print(f"🔍 Escaneando TCP en {ip} con detección de versiones de servicio...")
    resultado = subprocess.run(
        ["sudo", "nmap", "-sS", "-sV", "--top-ports", "100", "-O", "--osscan-guess", "--max-os-tries", "1", ip],  
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
    """Analiza la salida de Nmap y extrae información detallada sobre los servicios."""
    if not salida:
        return [], "No disponible", []

    so_match = re.findall(r"Aggressive OS guesses: (.+)", salida)
    sistemas_operativos = so_match[0].split(", ")[:3] if so_match else ["Desconocido"]

    fingerprint_match = re.search(r"TCP/IP fingerprint:\n(.*)", salida, re.DOTALL)
    fingerprint = fingerprint_match.group(1).strip() if fingerprint_match else "No disponible"

    puertos_abiertos = []
    for linea in salida.split("\n"):
        puerto_match = re.match(r"(\d+)/(tcp|udp)\s+open\s+([\w-]+)\s*(.*)", linea)
        if puerto_match:
            puertos_abiertos.append({
                "puerto": int(puerto_match.group(1)),
                "protocolo": puerto_match.group(2),
                "servicio": puerto_match.group(3),
                "version": puerto_match.group(4).strip() if puerto_match.group(4) else "No detectada"
            })

    return sistemas_operativos, fingerprint, puertos_abiertos

def escanear_dispositivo(ip, mac):
    """Ejecuta los escaneos de TCP y UDP por separado para optimizar velocidad."""
    if not verificar_instalacion("nmap"):
        print("Error: Nmap no está instalado.")
        return None

    print(f"🚀 Iniciando escaneo de {ip} (MAC: {mac})...")

    fabricante = obtener_fabricante(mac)

    salida_tcp = escanear_tcp(ip)
    so_tcp, fingerprint_tcp, puertos_tcp = analizar_salida_nmap(salida_tcp)

    salida_udp = escanear_udp(ip)
    _, _, puertos_udp = analizar_salida_nmap(salida_udp)

    return {
        "ip": ip,
        "mac": mac,
        "fabricante": fabricante,
        "sistemas_operativos": so_tcp,
        "fingerprint": fingerprint_tcp,
        "puertos_abiertos": puertos_tcp + puertos_udp  
    }

if __name__ == "__main__":

    resultados = []

    for dispositivo in dispositivos_activos:
        info_dispositivo = escanear_dispositivo(dispositivo["ip"], dispositivo["mac"])
        if info_dispositivo:
            resultados.append(info_dispositivo)

    # ✅ Ahora llamamos a la función específica para Nmap
    procesar_y_guardar_nmap(resultados)
