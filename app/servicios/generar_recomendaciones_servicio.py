from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.dispositivo import Dispositivo
from app.modelos.puerto_abierto import PuertoAbierto
from app.modelos.recomendacion_puerto import RecomendacionPuerto
from app.servicios.gemini_servicio import generar_respuesta_gemini
from app.core.base_datos import SesionLocal

def obtener_dispositivo_por_id(db: Session, dispositivo_id: int):
    """🔍 Obtiene un dispositivo por su ID."""
    dispositivo = db.query(Dispositivo).filter(Dispositivo.dispositivo_id == dispositivo_id, Dispositivo.estado == True).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail=f"Dispositivo con ID {dispositivo_id} no encontrado o inactivo.")
    return dispositivo

def obtener_puertos_abiertos(db: Session, dispositivo_id: int):
    """🔍 Obtiene los puertos abiertos de un dispositivo."""
    return db.query(PuertoAbierto).filter(PuertoAbierto.dispositivo_id == dispositivo_id).all()

def obtener_recomendacion_existente(db: Session, puerto_id: int):
    """🔍 Verifica si ya existe una recomendación para un puerto."""
    return db.query(RecomendacionPuerto).filter(RecomendacionPuerto.puerto_id == puerto_id).first()

def generar_recomendacion_con_gemini(puerto: PuertoAbierto):
    """🔍 Usa Gemini para analizar un puerto y generar una recomendación solo si es necesario."""
    prompt = (
        f"Proporciona una recomendación de seguridad para el puerto {puerto.puerto}. "
        "Explica brevemente qué acciones tomar para mitigar riesgos. "
        "La respuesta debe ser clara y concisa, sin mencionar 'Recomendación de seguridad para el puerto' ni repetir el número del puerto."
    )
    
    print(f"[INFO] Generando recomendación para el puerto {puerto.puerto} en dispositivo {puerto.dispositivo_id}...")
    respuesta = generar_respuesta_gemini(prompt).strip()
    
    # Limpieza de la respuesta
    palabras_clave = ["Recomendación:", "Seguridad:", "**Recomendación**", "**Recomendación de Seguridad**"]
    for palabra in palabras_clave:
        if respuesta.startswith(palabra):
            respuesta = respuesta[len(palabra):].strip()
    
    print(f"[INFO] Recomendación generada: {respuesta}")
    return respuesta

def guardar_recomendacion(db: Session, puerto_id: int, recomendacion: str):
    """💾 Guarda la recomendación en la base de datos."""
    print(f"[INFO] Guardando nueva recomendación para el puerto {puerto_id}...")
    nueva_recomendacion = RecomendacionPuerto(
        puerto_id=puerto_id,
        recomendacion=recomendacion
    )
    db.add(nueva_recomendacion)
    db.commit()
    print("[INFO] Recomendación guardada correctamente.")

def generar_recomendacion_por_puerto(db: Session, puerto_id: int):
    """🔍 Genera una recomendación solo para un puerto específico si no existe previamente."""
    puerto = db.query(PuertoAbierto).filter(PuertoAbierto.puerto_id == puerto_id).first()
    if not puerto:
        raise HTTPException(status_code=404, detail=f"Puerto con ID {puerto_id} no encontrado.")
    
    # ✅ Verificar si ya existe una recomendación antes de llamar a Gemini
    if obtener_recomendacion_existente(db, puerto_id):
        print(f"[INFO] Recomendación ya existe para el puerto {puerto_id}, omitiendo generación.")
        return {"message": "Recomendación ya existente, no se generó una nueva."}

    # ❌ No hay recomendación, generamos una nueva con Gemini
    recomendacion = generar_recomendacion_con_gemini(puerto)
    guardar_recomendacion(db, puerto.puerto_id, recomendacion)
    return {"message": "Recomendación generada con éxito.", "puerto": puerto.puerto, "recomendacion": recomendacion}

def generar_recomendaciones_por_dispositivo(db: Session, dispositivo_id: int):
    """🔥 Genera recomendaciones para todos los puertos de un dispositivo, evitando repeticiones."""
    dispositivo = obtener_dispositivo_por_id(db, dispositivo_id)
    puertos_abiertos = obtener_puertos_abiertos(db, dispositivo_id)
    
    if not puertos_abiertos:
        raise HTTPException(status_code=404, detail=f"No se encontraron puertos abiertos en el dispositivo {dispositivo_id}.")
    
    recomendaciones = []
    for puerto in puertos_abiertos:
        # 🔍 Revisamos si ya existe una recomendación para este puerto
        if obtener_recomendacion_existente(db, puerto.puerto_id):
            print(f"[INFO] Recomendación ya existente para el puerto {puerto.puerto}, se omite la generación.")
            continue  # **Seguimos con el siguiente puerto**

        # 🔥 Si no hay recomendación, la generamos
        recomendacion = generar_recomendacion_con_gemini(puerto)
        guardar_recomendacion(db, puerto.puerto_id, recomendacion)
        recomendaciones.append({"puerto": puerto.puerto, "recomendacion": recomendacion})
    
    return {"message": "Recomendaciones generadas con éxito.", "dispositivo": dispositivo_id, "recomendaciones": recomendaciones}

def generar_recomendaciones_por_puertos_seleccionados(db: Session, puertos_ids: list[int]):
    """🔍 Genera recomendaciones **solo para los puertos seleccionados** por el usuario."""
    if not puertos_ids:
        raise HTTPException(status_code=400, detail="Debe proporcionar al menos un puerto para generar recomendaciones.")

    recomendaciones = []
    for puerto_id in puertos_ids:
        # Obtener el puerto de la base de datos
        puerto = db.query(PuertoAbierto).filter(PuertoAbierto.puerto_id == puerto_id).first()
        if not puerto:
            print(f"[ERROR] Puerto con ID {puerto_id} no encontrado, se omite.")
            continue

        # Si ya existe una recomendación, no la generamos de nuevo
        if obtener_recomendacion_existente(db, puerto_id):
            print(f"[INFO] Recomendación ya existe para el puerto {puerto_id}, se omite la generación.")
            continue  

        # Generar la recomendación con Gemini
        recomendacion = generar_recomendacion_con_gemini(puerto)
        guardar_recomendacion(db, puerto_id, recomendacion)
        recomendaciones.append({"puerto": puerto.puerto, "recomendacion": recomendacion})

    return {"message": "Recomendaciones generadas con éxito.", "puertos": puertos_ids, "recomendaciones": recomendaciones}

# ✅ **EJECUTAR EL SCRIPT DIRECTAMENTE**
if __name__ == "__main__":
    print("[INFO] Iniciando generación de recomendaciones con Gemini...")
    db = SesionLocal()
    try:
        dispositivo_id = 1  # Cambiar esto por el ID de prueba
        generar_recomendaciones_por_dispositivo(db, dispositivo_id)
    except Exception as e:
        print(f"[ERROR] {str(e)}")
    finally:
        db.close()
