from scapy.all import rdpcap, IP, TCP, UDP
import json
import pandas as pd
from decimal import Decimal

def procesar_pcap(archivo_pcap):
    """Lee y extrae información clave de un archivo de captura .pcap."""
    paquetes = rdpcap(archivo_pcap)  # Leer archivo .pcap
    datos_paquetes = []

    for pkt in paquetes:
        datos = {
            "timestamp": float(pkt.time) if hasattr(pkt, 'time') else 0.0,
            "ip_origen": pkt[IP].src if pkt.haslayer(IP) else "Desconocido",
            "ip_destino": pkt[IP].dst if pkt.haslayer(IP) else "Desconocido",
            "puerto_origen": pkt[TCP].sport if pkt.haslayer(TCP) else (pkt[UDP].sport if pkt.haslayer(UDP) else "N/A"),
            "puerto_destino": pkt[TCP].dport if pkt.haslayer(TCP) else (pkt[UDP].dport if pkt.haslayer(UDP) else "N/A"),
            "protocolo": "TCP" if pkt.haslayer(TCP) else ("UDP" if pkt.haslayer(UDP) else "Otro"),
            "tamano": len(pkt)  # Tamaño del paquete en bytes
        }
        datos_paquetes.append(datos)

    return datos_paquetes

def guardar_json(datos, nombre_archivo="captura_procesada.json"):
    """Guarda los datos en un archivo JSON asegurando que sean serializables."""
    with open(nombre_archivo, "w") as f:
        json.dump(datos, f, indent=4)
    print(f"📂 Datos guardados en {nombre_archivo}")

def guardar_csv(datos, nombre_archivo="captura_procesada.csv"):
    """Guarda los datos en un archivo CSV para análisis más fácil."""
    df = pd.DataFrame(datos)
    df.to_csv(nombre_archivo, index=False)
    print(f"📂 Datos guardados en {nombre_archivo}")

if __name__ == "__main__":
    archivo_pcap = "captura.pcap"  # Archivo generado por TCPDump
    print("📊 Procesando archivo PCAP...")
    datos_procesados = procesar_pcap(archivo_pcap)

    if datos_procesados:
        guardar_json(datos_procesados)
        guardar_csv(datos_procesados)
    else:
        print("⚠️ No se encontraron paquetes en el archivo PCAP.")
