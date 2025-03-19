from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.configuracion_escaneo import ConfiguracionEscaneo
from app.esquemas.configuracion_escaneos_esquemas import ConfiguracionEscaneoCrear, ConfiguracionEscaneoActualizar

# 📌 Crear configuración de escaneo
def crear_configuracion_escaneo(datos: ConfiguracionEscaneoCrear, db: Session):
    nueva_configuracion = ConfiguracionEscaneo(**datos.dict())
    db.add(nueva_configuracion)
    db.commit()
    db.refresh(nueva_configuracion)
    return nueva_configuracion

# 📌 Actualizar configuración de escaneo
def actualizar_configuracion_escaneo(configuracion_id: int, datos: ConfiguracionEscaneoActualizar, db: Session):
    configuracion = db.query(ConfiguracionEscaneo).filter(ConfiguracionEscaneo.configuracion_escaneo_id == configuracion_id).first()
    if not configuracion:
        raise HTTPException(status_code=404, detail="Configuración de escaneo no encontrada")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(configuracion, key, value)
    
    db.commit()
    db.refresh(configuracion)
    return configuracion

# 📌 Obtener configuración por ID
def obtener_configuracion_escaneo(configuracion_id: int, db: Session):
    configuracion = db.query(ConfiguracionEscaneo).filter(ConfiguracionEscaneo.configuracion_escaneo_id == configuracion_id).first()
    if not configuracion:
        raise HTTPException(status_code=404, detail="Configuración de escaneo no encontrada")
    return configuracion

# 📌 Listar todas las configuraciones
def listar_configuraciones_escaneo(db: Session):
    return db.query(ConfiguracionEscaneo).order_by(ConfiguracionEscaneo.fecha_creacion.desc()).all()

# 📌 Eliminar configuración de escaneo
def eliminar_configuracion_escaneo(configuracion_id: int, db: Session):
    configuracion = db.query(ConfiguracionEscaneo).filter(ConfiguracionEscaneo.configuracion_escaneo_id == configuracion_id).first()
    if not configuracion:
        raise HTTPException(status_code=404, detail="Configuración de escaneo no encontrada")
    
    db.delete(configuracion)
    db.commit()
    return {"mensaje": "Configuración de escaneo eliminada exitosamente"}
