import json
import pandas as pd
import re
from pathlib import Path

def limpiar_servicio(servicio):
    if not servicio or servicio.lower() in ["unknown", "no disponible"]:
        return "Desconocido"
    servicio = re.sub(r'[?!]+$', '', servicio.strip())
    return servicio if servicio else "Desconocido"

def limpiar_version(version):
    if not version or version.lower() in ["no disponible", "unknown", ""]:
        return "Desconocido"
    return version.strip()

def limpiar_so(so):
    return so if so else "Desconocido"

def limpiar_vulnerabilidades(vulns):
    ids_vistos = set()
    vulns_limpias = []
    for v in vulns:
        vid = v.get("id")
        if vid and vid not in ids_vistos:
            ids_vistos.add(vid)
            vulns_limpias.append(v)
    return vulns_limpias

def limpiar_resultados_nmap(path_entrada: str | Path, path_salida: str | Path) -> list:
    path_entrada = Path(path_entrada)
    path_salida = Path(path_salida)

    with path_entrada.open('r', encoding='utf-8') as f:
        data = json.load(f)

    resultados_limpios = []

    for host in data:
        ip = host.get("ip")
        sistema_operativo = limpiar_so(host.get('sistema_operativo'))

        puertos_info = []
        for servicio in host.get('servicios', []):
            puerto = servicio.get("puerto")
            nombre_servicio = limpiar_servicio(servicio.get('servicio'))
            version = limpiar_version(servicio.get('version'))

            # Buscar vulnerabilidades asociadas al mismo puerto
            vulnerabilidades_puerto = []
            for vuln in host.get('vulnerabilidades', []):
                if vuln.get("puerto") == puerto:
                    limpias = limpiar_vulnerabilidades(vuln.get("vulnerabilidades", []))
                    vulnerabilidades_puerto.extend(limpias)

            puertos_info.append({
                "puerto": puerto,
                "servicio": nombre_servicio,
                "version": version,
                "vulnerabilidades": vulnerabilidades_puerto
            })

        resultados_limpios.append({
            "ip": ip,
            "sistema_operativo": sistema_operativo,
            "puertos": puertos_info
        })

    with path_salida.open('w', encoding='utf-8') as f:
        json.dump(resultados_limpios, f, indent=2, ensure_ascii=False)

    print(f"✅ Archivo limpio guardado en: {path_salida}")
    return resultados_limpios

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent  # app/utils desde pandas
    entrada = BASE_DIR / "nmap" / "nmap_resultados.json"
    salida = BASE_DIR / "pandas" / "nmap_resultados_limpio.json"
    limpiar_resultados_nmap(entrada, salida)
