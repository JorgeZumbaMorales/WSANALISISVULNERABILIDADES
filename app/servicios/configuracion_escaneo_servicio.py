from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.configuracion_escaneo import ConfiguracionEscaneo
from app.esquemas.configuracion_escaneo_esquemas import ConfiguracionEscaneoCrear, ConfiguracionEscaneoActualizar

def crear_configuracion_escaneo(datos: ConfiguracionEscaneoCrear, db: Session):
    nueva_configuracion = ConfiguracionEscaneo(
        tipo_escaneo_id=datos.tipo_escaneo_id
    )
    db.add(nueva_configuracion)
    db.commit()
    db.refresh(nueva_configuracion)
    return nueva_configuracion

def obtener_configuracion_escaneo(db: Session, configuracion_id: int):
    configuracion = db.query(ConfiguracionEscaneo).filter(
        ConfiguracionEscaneo.configuracion_escaneo_id == configuracion_id
    ).first()
    
    if not configuracion:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    
    return configuracion

def actualizar_configuracion_escaneo(configuracion_id: int, datos: ConfiguracionEscaneoActualizar, db: Session):
    configuracion = obtener_configuracion_escaneo(db, configuracion_id)
    
    if datos.estado is not None:
        configuracion.estado = datos.estado
    
    db.commit()
    db.refresh(configuracion)
    return configuracion

def eliminar_configuracion_escaneo(configuracion_id: int, db: Session):
    configuracion = obtener_configuracion_escaneo(db, configuracion_id)
    db.delete(configuracion)
    db.commit()
    return {"message": "Configuración eliminada exitosamente"}

def listar_configuraciones(db: Session):
    return db.query(ConfiguracionEscaneo).all()
