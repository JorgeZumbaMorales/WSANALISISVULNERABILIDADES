from sqlalchemy.orm import Session
from app.modelos.configuracion_escaneo import ConfiguracionEscaneo
from fastapi import HTTPException

def obtener_configuracion_escaneo(db: Session):
    """
    Obtiene la configuración de escaneo activa en la base de datos.
    """
    configuracion = db.query(ConfiguracionEscaneo).filter(ConfiguracionEscaneo.estado == True).first()
    
    if not configuracion:
        raise HTTPException(status_code=404, detail="No hay una configuración de escaneo activa")
    
    return {
        "tipo_escaneo_id": configuracion.tipo_escaneo_id,
        "frecuencia_minutos": configuracion.frecuencia_minutos,
        "hora_especifica": str(configuracion.hora_especifica) if configuracion.hora_especifica else None
    }
