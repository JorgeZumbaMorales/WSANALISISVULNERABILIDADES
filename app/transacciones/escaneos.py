import json
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from datetime import datetime
from app.core.base_datos import SesionLocal

# 🔹 Importamos los servicios correctos
from app.servicios.dispositivo_servicio import (
    crear_dispositivo,
    obtener_dispositivo_por_mac,
    actualizar_estado_dispositivo
)
from app.servicios.ip_asignacion_servicio import (
    registrar_nueva_ip,
    obtener_ultima_ip_dispositivo
)
from app.servicios.puerto_abierto_servicio import crear_puerto_abierto
from app.servicios.sistema_operativo_servicio import obtener_sistema_operativo_por_nombre
from app.servicios.dispositivo_sistema_operativo_servicio import crear_dispositivo_sistema_operativo

# Importamos los esquemas correctos
from app.esquemas.dispositivo_esquemas import DispositivoCrear, DispositivoActualizarEstado
from app.esquemas.puerto_abierto_esquemas import PuertoAbiertoCrear
from app.esquemas.dispositivo_sistema_operativo_esquemas import DispositivoSistemaOperativoCrear
# Importamos los modelos correctos
from app.modelos.dispositivo import Dispositivo


def procesar_resultados(db: Session, archivo_json: str):
    """
    📌 Procesa el archivo JSON de resultados del escaneo y guarda los datos en la base de datos.
    También actualiza el estado de dispositivos que no aparecen en el escaneo.
    """
    try:
        with open(archivo_json, "r", encoding="utf-8") as f:
            datos = json.load(f)

        if not datos:
            print("[ERROR] No hay datos en el archivo JSON.")
            return

        print(f"[INFO] Procesando {len(datos)} dispositivos encontrados...")
        print(f"[DEBUG] Datos leídos del JSON: {datos}")

        macs_actuales = {dispositivo["mac_address"] for dispositivo in datos}

        # **1️⃣ Desactivar dispositivos que no fueron encontrados en el escaneo**
        dispositivos_en_bd = db.query(Dispositivo).all()

        # 🛑 Antes de empezar la transacción, verificamos si la sesión está activa
        if db.in_transaction():
            print("[ERROR] ❌ ¡La sesión ya tiene una transacción activa! Abortando...")
            return

        with db.begin():  # 🔹 Se maneja una transacción global para la inserción de nuevos datos
            print("[DEBUG] Iniciando transacción para guardar nuevos datos...")

            # **2️⃣ Procesar cada dispositivo encontrado en el escaneo**
            for dispositivo in datos:
                ip_actual = dispositivo["ip_address"]
                mac = dispositivo["mac_address"]
                so_nombre = dispositivo["sistema_operativo"]

                dispositivo_existente = obtener_dispositivo_por_mac(db, mac)

                if not dispositivo_existente:
                    datos_dispositivo = DispositivoCrear(
                        nombre_dispositivo=f"Dispositivo-{mac[-4:]}",  
                        mac_address=mac
                    )
                    dispositivo_bd = crear_dispositivo(datos_dispositivo, db)
                else:
                    dispositivo_bd = dispositivo_existente
                    if not dispositivo_bd.estado:
                        dispositivo_bd.estado = True  # ✅ Cambiamos estado sin hacer commit
                        db.flush()  # ✅ Guardar temporalmente en la transacción sin hacer commit

                # **Registrar el sistema operativo en `dispositivo_sistema_operativo`**
                sistema_operativo = obtener_sistema_operativo_por_nombre(db, so_nombre)

                if sistema_operativo:  # Verificar que el SO existe en la BD
                    datos_so_dispositivo = DispositivoSistemaOperativoCrear(
                        dispositivo_id=dispositivo_bd.dispositivo_id,
                        sistema_operativo_id=sistema_operativo.sistema_operativo_id
                    )
                    crear_dispositivo_sistema_operativo(datos_so_dispositivo, db)  # ✅ Insertar en la tabla
                else:
                    print(f"[WARN] Sistema operativo '{so_nombre}' no encontrado en la BD.")

                # **Registrar la IP en `ip_asignaciones` solo si es diferente**
                ultima_ip = obtener_ultima_ip_dispositivo(db, dispositivo_bd.dispositivo_id)
                if ultima_ip != ip_actual:
                    registrar_nueva_ip(mac, ip_actual, db)  # ✅ Ya no hace commit dentro

                # **Guardar los puertos abiertos**
                for puerto in dispositivo["puertos_abiertos"]:
                    datos_puerto = PuertoAbiertoCrear(
                        dispositivo_id=dispositivo_bd.dispositivo_id,
                        puerto=puerto["puerto"],
                        protocolo=puerto["protocolo"].upper(),
                        servicio=puerto["servicio"],
                        version=puerto["version"]
                    )
                    crear_puerto_abierto(datos_puerto, db)

            print("[DEBUG] Confirmando transacción en la BD...")

        print("[INFO] Datos guardados en la base de datos exitosamente.")

    except (SQLAlchemyError, json.JSONDecodeError) as e:
        db.rollback()  # 🔴 **Revertir cambios en caso de error**
        print(f"[ERROR] Error al procesar los resultados: {e}")
        raise HTTPException(status_code=500, detail=f"Error al guardar en la BD: {str(e)}")


if __name__ == "__main__":
    print("[INFO] Ejecutando procesamiento de resultados...")

    db = SesionLocal()
    archivo_json = "app/utils/nmap_resultados.json"  # Ruta donde se guarda el JSON

    procesar_resultados(db, archivo_json)
