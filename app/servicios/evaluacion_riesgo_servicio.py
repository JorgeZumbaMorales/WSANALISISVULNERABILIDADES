from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.dispositivo import Dispositivo
from app.modelos.puerto_abierto import PuertoAbierto
from app.modelos.riesgo import Riesgo
from app.modelos.dispositivo_riesgo import DispositivoRiesgo
from app.servicios.gemini_servicio import generar_respuesta_gemini
from app.core.base_datos import SesionLocal  # ✅ Importamos la sesión de BD

def obtener_dispositivos_activos(db: Session):
    """🔍 Obtiene todos los dispositivos activos en la base de datos."""
    dispositivos = db.query(Dispositivo).filter(Dispositivo.estado == True).all()
    print(f"[INFO] Se encontraron {len(dispositivos)} dispositivos activos.")
    return dispositivos

def obtener_puertos_abiertos(db: Session, dispositivo_id: int):
    """🔍 Obtiene los puertos abiertos de un dispositivo."""
    puertos = db.query(PuertoAbierto).filter(PuertoAbierto.dispositivo_id == dispositivo_id).all()
    print(f"[INFO] Dispositivo {dispositivo_id} tiene {len(puertos)} puertos abiertos.")
    return puertos

def evaluar_riesgo_con_gemini(puertos: list):
    """🔍 Usa Gemini para analizar los puertos abiertos y determinar el riesgo."""
    if not puertos:
        print("[INFO] No hay puertos abiertos, asignando 'Sin Riesgo'.")
        return "Sin Riesgo"
    
    # Crear el mensaje para Gemini
    descripcion_puertos = "\n".join([f"Puerto {p.puerto}, Protocolo: {p.protocolo}, Servicio: {p.servicio}" for p in puertos])
    prompt = ("Analiza el siguiente conjunto de puertos abiertos en un dispositivo y clasifícalo en uno de estos niveles de riesgo: 'Alto', 'Medio', 'Bajo', 'Sin Riesgo'. "
              "Solo responde con uno de estos valores sin explicaciones adicionales. "
              "Puertos abiertos:\n" + descripcion_puertos)

    print("[INFO] Enviando consulta a Gemini...")
    respuesta = generar_respuesta_gemini(prompt).strip()
    print(f"[INFO] Respuesta de Gemini: {respuesta}")
    return respuesta

def obtener_riesgo_id(db: Session, nombre_riesgo: str):
    """🔍 Obtiene el ID del riesgo en base a su nombre ('Alto', 'Medio', etc.)."""
    print(f"[INFO] Buscando ID para el nivel de riesgo '{nombre_riesgo}'...")
    riesgo = db.query(Riesgo).filter(Riesgo.nombre_riesgo == nombre_riesgo).first()
    if not riesgo:
        print(f"[ERROR] No se encontró el riesgo '{nombre_riesgo}'.")
        raise HTTPException(status_code=404, detail=f"No se encontró el riesgo '{nombre_riesgo}'")
    print(f"[INFO] ID del riesgo '{nombre_riesgo}': {riesgo.riesgo_id}")
    return riesgo.riesgo_id

def evaluar_riesgo_dispositivos(db: Session):
    """🔥 Evalúa el riesgo de todos los dispositivos y lo guarda en `dispositivo_riesgo`."""
    dispositivos = obtener_dispositivos_activos(db)

    for dispositivo in dispositivos:
        print(f"\n[INFO] Evaluando dispositivo {dispositivo.dispositivo_id} ({dispositivo.mac_address})...")
        puertos_abiertos = obtener_puertos_abiertos(db, dispositivo.dispositivo_id)
        nivel_riesgo = evaluar_riesgo_con_gemini(puertos_abiertos)
        riesgo_id = obtener_riesgo_id(db, nivel_riesgo)

        registro_existente = db.query(DispositivoRiesgo).filter(
            DispositivoRiesgo.dispositivo_id == dispositivo.dispositivo_id
        ).first()

        if registro_existente:
            print(f"[INFO] Actualizando riesgo para dispositivo {dispositivo.dispositivo_id}.")
            registro_existente.riesgo_id = riesgo_id
        else:
            print(f"[INFO] Insertando nuevo riesgo para dispositivo {dispositivo.dispositivo_id}.")
            nuevo_registro = DispositivoRiesgo(
                dispositivo_id=dispositivo.dispositivo_id,
                riesgo_id=riesgo_id
            )
            db.add(nuevo_registro)

    db.commit()
    print("[INFO] Evaluación de riesgos completada y guardada en la base de datos.")
    return {"mensaje": "Evaluación de riesgos completada usando Gemini."}

# ✅ **EJECUTAR EL SCRIPT DIRECTAMENTE**
if __name__ == "__main__":
    print("[INFO] Iniciando evaluación de riesgos con Gemini...")

    db = SesionLocal()
    try:
        resultado = evaluar_riesgo_dispositivos(db)
        print(resultado)
    except Exception as e:
        print(f"[ERROR] {str(e)}")
    finally:
        db.close()
