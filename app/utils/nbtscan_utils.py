import subprocess
import shutil
import re

def verificar_instalacion(comando):
    """Verifica si un comando está instalado en el sistema."""
    return shutil.which(comando) is not None

def obtener_nombre_dispositivo(ip):
    """Obtiene el nombre NetBIOS del dispositivo en redes Windows."""
    if not verificar_instalacion("nbtscan"):
        print("Error: nbtscan no está instalado. Instálalo con 'sudo apt install nbtscan' en Linux.")
        return "No disponible"
    
    try:
        print(f"🔍 Escaneando nombre NetBIOS de {ip} con nbtscan...")
        resultado = subprocess.run(
            ["sudo", "nbtscan", "-r", ip],  # ✅ Se agrega "sudo"
            text=True,
            capture_output=True
        )
        
        if resultado.returncode != 0:
            print(f"Error ejecutando nbtscan: {resultado.stderr}")
            return "No disponible"

        salida = resultado.stdout
        match = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([^\s]+)", salida)
        if match:
            return match.group(2)  # Devuelve el nombre del dispositivo

    except Exception as e:
        print(f"Error obteniendo nombre del dispositivo: {e}")

    return "No disponible"


if __name__ == "__main__":
    # Ejemplo de prueba
    ip_prueba = "192.168.1.10"
    nombre = obtener_nombre_dispositivo(ip_prueba)
    print(f"📌 Dispositivo {ip_prueba} identificado como: {nombre}")
