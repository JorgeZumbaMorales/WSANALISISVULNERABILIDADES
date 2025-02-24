import json
import pandas as pd

def guardar_json_nmap(datos, nombre_archivo="nmap_resultados.json"):
    """Guarda los datos escaneados con Nmap en formato JSON."""
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f"📂 Datos de Nmap guardados en {nombre_archivo}")

def guardar_csv_nmap(datos, nombre_archivo="nmap_resultados.csv"):
    """Guarda los datos escaneados con Nmap en formato CSV."""
    df = pd.DataFrame(datos)
    df.to_csv(nombre_archivo, index=False)
    print(f"📂 Datos de Nmap guardados en {nombre_archivo}")

def procesar_y_guardar_nmap(datos):
    """Procesa y guarda los datos de Nmap en los formatos deseados."""
    if not datos:
        print("⚠️ No hay datos de Nmap para guardar.")
        return

    guardar_json_nmap(datos)
    guardar_csv_nmap(datos)

