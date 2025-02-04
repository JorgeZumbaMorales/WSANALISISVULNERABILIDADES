import subprocess
import os

def verificar_nmap_instalado():
    """
    Verifica si nmap está instalado en el sistema operativo.
    """
    try:
        resultado = subprocess.run(["nmap", "--version"], capture_output=True, text=True, check=True)
        print("Nmap está instalado:", resultado.stdout.splitlines()[0])
        return True
    except FileNotFoundError:
        print("Nmap no está instalado en el sistema operativo.")
        return False
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar nmap:", e)
        return False

def verificar_permisos_root():
    """
    Verifica si el script tiene permisos de superusuario.
    """
    if os.geteuid() != 0:
        print("Advertencia: Este script requiere permisos de superusuario para ciertos tipos de escaneo.")
        return False
    return True

def ejecutar_nmap(ips, opciones="-sT"):
    """
    Ejecuta un escaneo de nmap en las IPs proporcionadas con las opciones especificadas.
    """
    if not ips or not isinstance(ips, list):
        raise ValueError("La lista de IPs debe ser un arreglo no vacío.")
    
    comando = ["nmap"] + opciones.split() + ips
    print(f"Ejecutando comando: {' '.join(comando)}")
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        print("Resultado del escaneo:\n", resultado.stdout)
        return resultado.stdout
    except FileNotFoundError:
        print("Error: Nmap no está instalado.")
        return None
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar nmap:", e.stderr)
        return None
    except PermissionError:
        print("Error: Permisos insuficientes para ejecutar nmap.")
        return None

def detectar_dispositivos(rango_red="192.168.1.0/24"):
    """
    Detecta dispositivos activos en la red dada.
    """
    comando = ["nmap", "-sn", rango_red]
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        dispositivos = []
        for linea in resultado.stdout.splitlines():
            if "Nmap scan report for" in linea:
                dispositivos.append(linea.split("for")[-1].strip())
        print(f"Dispositivos detectados en la red {rango_red}:\n", dispositivos)
        return dispositivos
    except subprocess.CalledProcessError as e:
        print("Error al detectar dispositivos:", e.stderr)
        return []

def obtener_detalles_dispositivo(ip):
    """
    Obtiene detalles de un dispositivo en la red.
    """
    comando = ["nmap", "-A", ip]
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        if "0 IP addresses" in resultado.stdout:
            print(f"El host {ip} no respondió. Intentando con -Pn...")
            comando = ["nmap", "-Pn", "-A", ip]
            resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        print(f"Detalles del dispositivo ({ip}):\n", resultado.stdout)
        return resultado.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error al obtener detalles del dispositivo {ip}:", e.stderr)
        return None

def analizar_resultados(detalles):
    """
    Analiza los resultados de un escaneo de Nmap y extrae información relevante.
    """
    if "Host is up" in detalles:
        print("El dispositivo está activo.")
    if "PORT" in detalles:
        print("Puertos abiertos detectados:")
        for linea in detalles.splitlines():
            if "/tcp" in linea:
                print(linea)  
                
if __name__ == "__main__":
    if verificar_nmap_instalado():
        print("Detectando dispositivos en la red local...")
        dispositivos = detectar_dispositivos("192.168.1.0/24")
        if dispositivos:
            print("Dispositivos detectados:")
            for dispositivo in dispositivos:
                print(dispositivo)
                # Obtener detalles de cada dispositivo
                detalles = obtener_detalles_dispositivo(dispositivo.split(" ")[-1])  # Toma la IP del dispositivo
                if detalles:
                    print("Detalles obtenidos:")
                    analizar_resultados(detalles)
        else:
            print("No se detectaron dispositivos en la red.")
