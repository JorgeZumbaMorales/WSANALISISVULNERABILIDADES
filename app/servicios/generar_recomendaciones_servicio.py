from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.dispositivo import Dispositivo
from app.modelos.puerto_abierto import PuertoAbierto
from app.modelos.recomendacion_puerto import RecomendacionPuerto
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

def generar_recomendacion_con_gemini(puerto: PuertoAbierto):
    """🔍 Usa Gemini para analizar un puerto y generar una recomendación."""
    prompt = (
        f"Proporciona una recomendación de seguridad para el puerto {puerto.puerto} "
        "Explica brevemente qué acciones tomar para mitigar riesgos. "
        "La respuesta debe ser clara y concisa, sin mencionar 'Recomendación de seguridad para el puerto' ni repetir el número del puerto."
    )

    print(f"[INFO] Generando recomendación para el puerto {puerto.puerto} en dispositivo {puerto.dispositivo_id}...")
    respuesta = generar_respuesta_gemini(prompt).strip()

    # ✅ Limpieza: eliminar encabezados no deseados
    palabras_clave = ["Recomendación:", "Seguridad:", "**Recomendación**", "**Recomendación de Seguridad**"]
    for palabra in palabras_clave:
        if respuesta.startswith(palabra):
            respuesta = respuesta[len(palabra):].strip()

    print(f"[INFO] Recomendación generada: {respuesta}")

    return respuesta


def guardar_recomendacion(db: Session, puerto_id: int, recomendacion: str):
    """💾 Guarda la recomendación en la base de datos."""
    print(f"[INFO] Guardando recomendación para el puerto {puerto_id}...")
    nueva_recomendacion = RecomendacionPuerto(
        puerto_id=puerto_id,
        recomendacion=recomendacion
    )
    db.add(nueva_recomendacion)
    db.commit()
    print("[INFO] Recomendación guardada correctamente.")

def generar_recomendaciones_dispositivos(db: Session):
    """🔥 Genera recomendaciones de seguridad para los puertos abiertos en los dispositivos."""
    dispositivos = obtener_dispositivos_activos(db)

    for dispositivo in dispositivos:
        print(f"\n[INFO] Generando recomendaciones para el dispositivo {dispositivo.dispositivo_id} ({dispositivo.mac_address})...")
        puertos_abiertos = obtener_puertos_abiertos(db, dispositivo.dispositivo_id)

        for puerto in puertos_abiertos:
            recomendacion = generar_recomendacion_con_gemini(puerto)
            guardar_recomendacion(db, puerto.puerto_id, recomendacion)

    print("[INFO] Generación de recomendaciones completada.")

# ✅ **EJECUTAR EL SCRIPT DIRECTAMENTE**
if __name__ == "__main__":
    print("[INFO] Iniciando generación de recomendaciones con Gemini...")

    db = SesionLocal()
    try:
        generar_recomendaciones_dispositivos(db)
    except Exception as e:
        print(f"[ERROR] {str(e)}")
    finally:
        db.close()
