import json
import os
from datetime import datetime
from typing import List
# ...otros imports ya existentes
from detectar_red_local import obtener_red_local
from escanear_hosts import escanear_hosts_activos
from escaneo_puertos import escanear_puertos
from detectar_servicios import detectar_servicios
from detectar_so import detectar_sistema_operativo
from buscar_cves import buscar_vulnerabilidades



def proceso_completo():
    red = obtener_red_local()
    if not red:
        print("[❌] No se pudo detectar la red local.")
        return

    print(f"[🔍] Iniciando escaneo en la red: {red}")
    hosts_activos = escanear_hosts_activos(red)
    
    if not hosts_activos:
        print("[⚠️] No se detectaron hosts activos.")
        return

    resultados = []

    for ip in hosts_activos:
        print(f"\n📡 Procesando host: {ip}")

        puertos = escanear_puertos(ip)
        servicios = detectar_servicios(ip, puertos)
        sistema_operativo = detectar_sistema_operativo(ip)
        cves = buscar_vulnerabilidades(ip, puertos)

        host_info = {
            "ip": ip,
            "puertos": puertos,
            "servicios": servicios,
            "sistema_operativo": sistema_operativo,
            "vulnerabilidades": cves
        }

        resultados.append(host_info)

    # Guardar los resultados en un JSON
    guardar_resultados_json(resultados)

    return resultados


def guardar_resultados_json(data: List[dict], nombre_archivo="nmap_resultados.json"):
    ruta_archivo = os.path.join(os.path.dirname(__file__), nombre_archivo)

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Resultados guardados en: {ruta_archivo}")



if __name__ == "__main__":
    proceso_completo()
