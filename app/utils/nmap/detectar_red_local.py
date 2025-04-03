import socket
import subprocess
import re


def obtener_red_local():
    """
    Detecta automáticamente la red local (ej. 192.168.1.0/24) usando la IP del equipo
    y su máscara de red detectada dinámicamente.
    """
    try:
        # 🔍 Detectar IP local conectándose a una IP externa
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_local = s.getsockname()[0]
        s.close()

        # 🧠 Obtener máscara de red (CIDR) usando `ip` de Linux
        resultado = subprocess.run(
            ["ip", "-o", "-f", "inet", "addr", "show"],
            capture_output=True,
            text=True
        )
        salida = resultado.stdout

        # 📦 Buscar la línea correspondiente a nuestra IP
        for linea in salida.split("\n"):
            if ip_local in linea:
                match = re.search(r"(\d+\.\d+\.\d+\.\d+)/(\d+)", linea)
                if match:
                    ip_base, prefijo = match.groups()
                    # 🔄 Reemplazar último octeto por 0
                    octetos = ip_base.split(".")
                    octetos[-1] = "0"
                    red = ".".join(octetos)
                    red_cidr = f"{red}/{prefijo}"
                    print(f"[INFO] Red local detectada automáticamente: {red_cidr}")
                    return red_cidr

        raise Exception("No se pudo determinar la máscara de subred.")

    except Exception as e:
        print(f"[ERROR] No se pudo detectar la red: {e}")
        return None
