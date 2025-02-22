import subprocess
import os
import shutil  # Para verificar disponibilidad de comandos

def verificar_tcpdump_instalado():
    """
    Verifica si tcpdump está instalado en el sistema operativo.
    """
    try:
        resultado = subprocess.run(["tcpdump", "--version"], capture_output=True, text=True, check=True)
        print("✅ TCPDump está instalado:", resultado.stdout.splitlines()[0])
        return True
    except FileNotFoundError:
        print("❌ TCPDump no está instalado en el sistema operativo.")
        return False
    except subprocess.CalledProcessError as e:
        print("⚠️ Error al ejecutar tcpdump:", e)
        return False

def listar_interfaces():
    """
    Lista las interfaces disponibles en el sistema para capturar tráfico.
    """
    try:
        resultado = subprocess.run(["tcpdump", "-D"], capture_output=True, text=True, check=True)
        interfaces = resultado.stdout.splitlines()
        nombres = []

        print("🔍 Interfaces disponibles:")
        for idx, interfaz in enumerate(interfaces):
            partes = interfaz.split(".", 1)
            if len(partes) > 1:
                nombre = partes[1].strip().split()[0]
                print(f"   {idx + 1}: {nombre}")
                nombres.append(nombre)
            else:
                print(f"⚠️ Advertencia: Formato inesperado para la línea: {interfaz}")

        return nombres
    except subprocess.CalledProcessError as e:
        print("⚠️ Error al listar interfaces:", e.stderr)
        return []

def capturar_paquetes(interface="wlp2s0", duracion=10, archivo_salida="captura.pcap"):
    """Captura tráfico en una interfaz con permisos elevados."""
    if not shutil.which("tcpdump"):
        print("❌ Error: TCPDump no está disponible en esta máquina.")
        return

    comando = ["sudo", "tcpdump", "-i", interface, "-w", archivo_salida, "-G", str(duracion), "-W", "1"]
    print(f"📡 Iniciando captura en la interfaz {interface} durante {duracion} segundos...")

    try:
        subprocess.run(comando, check=True)
        print(f"✅ Captura completada. Los datos están guardados en: {archivo_salida}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al capturar tráfico en {interface}: {e}")


# Solo ejecutar si el script es ejecutado directamente
if __name__ == "__main__":
    if verificar_tcpdump_instalado():
        interfaces = listar_interfaces()
        if interfaces:
            interfaz = interfaces[0]
            capturar_paquetes(interface=interfaz, duracion=10, archivo_salida="captura.pcap")
        else:
            print("⚠️ No se encontraron interfaces válidas para capturar tráfico.")
