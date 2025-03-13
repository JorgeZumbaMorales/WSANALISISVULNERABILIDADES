import subprocess
import json
import re
import os
import socket
import struct
import fcntl



def obtener_red_local():
    """ Detecta automáticamente la red local en la que se encuentra el equipo """
    try:
        # Obtener la dirección IP local usando socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Conectar a un servidor externo para determinar la interfaz activa
        ip_local = s.getsockname()[0]
        s.close()

        # Usar el comando `ip -o -f inet addr show` para obtener la máscara de subred
        resultado = subprocess.run(
            ["ip", "-o", "-f", "inet", "addr", "show"],
            capture_output=True,
            text=True
        )
        salida = resultado.stdout

        # Buscar la línea que contenga nuestra IP
        for linea in salida.split("\n"):
            if ip_local in linea:
                match = re.search(r"(\d+\.\d+\.\d+\.\d+)/(\d+)", linea)
                if match:
                    ip_base, prefijo = match.groups()
                    red = ".".join(ip_base.split(".")[:3]) + ".0"
                    red_cidr = f"{red}/{prefijo}"
                    print(f"[INFO] Red detectada automáticamente: {red_cidr}")
                    return red_cidr

        raise Exception("No se pudo determinar la máscara de subred.")

    except Exception as e:
        print(f"[ERROR] No se pudo detectar la red: {e}")
        return None

def ejecutar_nmap(archivo_salida="nmap_resultados.json"):
    red = obtener_red_local()
    if not red:
        print("[ERROR] No se puede ejecutar el escaneo sin una red válida.")
        return None

    print(f"[INFO] Ejecutando escaneo Nmap en la red {red}...")

    comando_nmap = f"sudo nmap -sS -sV -O -p- --min-rate 5000 {red}"

    try:
        resultado = subprocess.run(comando_nmap, shell=True, capture_output=True, text=True, check=True)
        salida_nmap = resultado.stdout
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error al ejecutar Nmap: {e}")
        return None

    dispositivos = []
    bloques = salida_nmap.split("Nmap scan report for ")

    for bloque in bloques[1:]:  # Ignorar primera parte vacía
        lineas = bloque.split("\n")

        # Extraer IP
        ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", lineas[0])
        ip = ip_match.group(0) if ip_match else "Desconocida"

        # Extraer MAC Address
        mac_match = re.search(r"MAC Address: ([0-9A-Fa-f:]+)", bloque)
        mac = mac_match.group(1) if mac_match else "No disponible"

        # Extraer Sistema Operativo
        os_match = re.search(r"OS details: (.+)", bloque)
        sistema_operativo = os_match.group(1) if os_match else "No disponible"

        # Extraer Puertos abiertos
        puertos_abiertos = []
        for linea in lineas:
            puerto_match = re.match(r"(\d+)/tcp\s+open\s+(\S+)\s*(.*)", linea)
            if puerto_match:
                puerto, servicio, version = puerto_match.groups()
                puertos_abiertos.append({
                    "puerto": int(puerto),
                    "protocolo": "tcp",
                    "servicio": servicio,
                    "version": version.strip() if version else "No disponible"
                })

        # Agregar dispositivo si tiene al menos un puerto abierto
        if puertos_abiertos:
            dispositivos.append({
                "ip_address": ip,
                "mac_address": mac,
                "sistema_operativo": sistema_operativo,
                "puertos_abiertos": puertos_abiertos
            })

    # Guardar en JSON
    with open(archivo_salida, "w", encoding="utf-8") as f:
        json.dump(dispositivos, f, indent=4)

    print(f"[INFO] Resultados guardados en {archivo_salida}")
    return archivo_salida

if __name__ == "__main__":
    ejecutar_nmap()
