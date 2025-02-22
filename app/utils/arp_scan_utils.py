import subprocess
import re
import shutil

def verificar_instalacion(comando):
    """Verifica si un comando está instalado en el sistema."""
    return shutil.which(comando) is not None

def obtener_red_actual():
    """Obtiene la dirección de la red en la que está conectado el dispositivo usando ip route."""
    try:
        resultado = subprocess.check_output("ip route | grep default", shell=True, text=True)
        interfaz = resultado.split()[4]
        resultado_ip = subprocess.check_output(f"ip -o -f inet addr show {interfaz}", shell=True, text=True)
        match = re.search(r'(\d+\.\d+\.\d+)\.\d+/\d+', resultado_ip)
        if match:
            return f"{match.group(1)}.0/24"
    except Exception as e:
        print(f"Error obteniendo la red actual: {e}")
    return None

def escanear_red():
    """Escanea la red usando arp-scan sin pedir contraseña y obtiene las IPs y direcciones MAC de los dispositivos conectados."""
    if not verificar_instalacion("arp-scan"):
        print("Error: arp-scan no está instalado. Instálalo con 'sudo apt install arp-scan' en Linux.")
        return []
    try:
        print("Ejecutando arp-scan...")
        resultado = subprocess.run(["sudo", "arp-scan", "--localnet"], text=True, capture_output=True)
        if resultado.returncode != 0:
            print(f"Error ejecutando arp-scan: {resultado.stderr}")
            return []
        
        dispositivos = []
        for linea in resultado.stdout.split('\n'):
            match = re.match(r'(\d+\.\d+\.\d+\.\d+)\s+([0-9A-Fa-f:]{17})\s+(.+)', linea)
            if match:
                dispositivos.append({
                    "ip": match.group(1),
                    "mac": match.group(2),
                    "fabricante": match.group(3).strip()
                })
        
        return dispositivos
    except Exception as e:
        print(f"Error escaneando la red: {e}")
    return []

if __name__ == "__main__":
    red_actual = obtener_red_actual()
    if red_actual:
        print(f"Escaneando la red: {red_actual}")
        dispositivos_activos = escanear_red()
        for dispositivo in dispositivos_activos:
            print(f"Dispositivo encontrado: IP={dispositivo['ip']} MAC={dispositivo['mac']} Fabricante={dispositivo['fabricante']}")
