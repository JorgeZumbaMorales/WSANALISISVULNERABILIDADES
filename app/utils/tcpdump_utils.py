import subprocess
import os

def verificar_tcpdump_instalado():
    """
    Verifica si tcpdump está instalado en el sistema operativo.
    """
    try:
        resultado = subprocess.run(["tcpdump", "--version"], capture_output=True, text=True, check=True)
        print("TCPDump está instalado:", resultado.stdout.splitlines()[0])
        return True
    except FileNotFoundError:
        print("TCPDump no está instalado en el sistema operativo.")
        return False
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar tcpdump:", e)
        return False

def verificar_permisos_root():
    """
    Verifica si el script tiene permisos de superusuario.
    """
    if os.geteuid() != 0:
        print("Advertencia: Este script requiere permisos de superusuario para capturar tráfico.")
        return False
    return True

def listar_interfaces():
    """
    Lista las interfaces disponibles en el sistema para capturar tráfico.
    """
    try:
        resultado = subprocess.run(["tcpdump", "-D"], capture_output=True, text=True, check=True)
        interfaces = resultado.stdout.splitlines()
        print("Interfaces disponibles:")
        nombres = []  # Lista para nombres procesados
        for idx, interfaz in enumerate(interfaces):
            if "." in interfaz:  # Si tiene índice válido
                partes = interfaz.split(".", 1)
                if len(partes) > 1:
                    nombre = partes[1].strip().split()[0]  # Extraer el nombre de la interfaz
                    print(f"{idx}: {nombre}")
                    nombres.append(nombre)
                else:
                    print(f"Advertencia: Formato inesperado para la línea: {interfaz}")
            else:
                print(f"Advertencia: Formato inesperado para la línea: {interfaz}")
        return nombres
    except subprocess.CalledProcessError as e:
        print("Error al listar interfaces:", e.stderr)
        return []

def capturar_paquetes(interface, duracion=10, archivo_salida="captura.pcap"):
    """
    Captura tráfico en una interfaz durante un tiempo específico.
    :param interface: Interfaz de red a utilizar para la captura (nombre exacto, e.g., wlp2s0).
    :param duracion: Duración de la captura en segundos.
    :param archivo_salida: Nombre del archivo para guardar la captura.
    """
    comando = ["tcpdump", "-i", interface, "-w", archivo_salida, "-G", str(duracion), "-W", "1"]
    print(f"Iniciando captura en la interfaz {interface} durante {duracion} segundos...")
    try:
        subprocess.run(comando, check=True)
        print(f"Captura completada. Los datos están guardados en {archivo_salida}.")
    except subprocess.CalledProcessError as e:
        print("Error al capturar paquetes:", e.stderr)

def leer_captura(archivo):
    """
    Lee un archivo de captura .pcap y muestra un resumen de los paquetes capturados.
    :param archivo: Nombre del archivo de captura.
    """
    comando = ["tcpdump", "-r", archivo]
    print(f"Leyendo archivo de captura: {archivo}")
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        print("Resumen de la captura:")
        print(resultado.stdout)
        return resultado.stdout
    except FileNotFoundError:
        print("El archivo de captura no existe.")
    except subprocess.CalledProcessError as e:
        print("Error al leer el archivo de captura:", e.stderr)

if __name__ == "__main__":
    if verificar_tcpdump_instalado():
        if verificar_permisos_root():
            interfaces = listar_interfaces()
            if interfaces:
                interfaz = interfaces[0]  # Seleccionar la primera interfaz válida
                capturar_paquetes(interface=interfaz, duracion=10, archivo_salida="captura.pcap")
                leer_captura("captura.pcap")
            else:
                print("No se encontraron interfaces válidas para capturar tráfico.")
        else:
            print("Ejecute este script con permisos de superusuario para capturar tráfico.")
