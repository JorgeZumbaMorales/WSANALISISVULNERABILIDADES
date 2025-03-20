from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.configuracion_escaneo import ConfiguracionEscaneo
from app.esquemas.configuracion_escaneos_esquemas import ConfiguracionEscaneoCrear, ConfiguracionEscaneoActualizar

# 📌 Crear configuración de escaneo
def crear_configuracion_escaneo(datos: ConfiguracionEscaneoCrear, db: Session):
    if datos.estado:  # ✅ Si la nueva configuración es activa, desactivar las anteriores
        db.query(ConfiguracionEscaneo).filter(ConfiguracionEscaneo.estado == True).update({"estado": False})
    
    nueva_configuracion = ConfiguracionEscaneo(
        nombre_configuracion_escaneo=datos.nombre_configuracion_escaneo,
        tipo_escaneo_id=datos.tipo_escaneo_id,
        frecuencia_minutos=datos.frecuencia_minutos,
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin,
        estado=datos.estado if datos.estado is not None else False  # ✅ Por defecto será False si no se envía
    )

    db.add(nueva_configuracion)
    db.commit()
    db.refresh(nueva_configuracion)
    return nueva_configuracion
# 📌 Obtener configuración de escaneo por ID
def obtener_configuracion_escaneo(configuracion_id: int, db: Session):
    configuracion = db.query(ConfiguracionEscaneo).filter(
        ConfiguracionEscaneo.configuracion_escaneo_id == configuracion_id
    ).first()

    if not configuracion:
        raise HTTPException(status_code=404, detail="Configuración de escaneo no encontrada")

    return configuracion

# 📌 Actualizar configuración de escaneo
def actualizar_configuracion_escaneo(configuracion_id: int, datos: ConfiguracionEscaneoActualizar, db: Session):
    configuracion = db.query(ConfiguracionEscaneo).filter(
        ConfiguracionEscaneo.configuracion_escaneo_id == configuracion_id
    ).first()

    if not configuracion:
        raise HTTPException(status_code=404, detail="Configuración de escaneo no encontrada")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(configuracion, key, value)

    db.commit()
    db.refresh(configuracion)
    return configuracion

# 📌 Listar todas las configuraciones
def listar_configuraciones_escaneo(db: Session):
    return db.query(ConfiguracionEscaneo).order_by(ConfiguracionEscaneo.fecha_creacion.desc()).all()

# 📌 Eliminar configuración de escaneo
def eliminar_configuracion_escaneo(configuracion_id: int, db: Session):
    configuracion = db.query(ConfiguracionEscaneo).filter(
        ConfiguracionEscaneo.configuracion_escaneo_id == configuracion_id
    ).first()

    if not configuracion:
        raise HTTPException(status_code=404, detail="Configuración de escaneo no encontrada")
    
    db.delete(configuracion)
    db.commit()
    return {"mensaje": "Configuración de escaneo eliminada exitosamente"}

def activar_configuracion_escaneo(configuracion_id: int, db: Session):
    # 🔹 Desactivar todas las configuraciones activas
    db.query(ConfiguracionEscaneo).filter(ConfiguracionEscaneo.estado == True).update({"estado": False})
    
    # 🔹 Activar la configuración seleccionada
    configuracion = db.query(ConfiguracionEscaneo).filter(ConfiguracionEscaneo.configuracion_escaneo_id == configuracion_id).first()
    
    if not configuracion:
        raise HTTPException(status_code=404, detail="Configuración de escaneo no encontrada")

    configuracion.estado = True
    db.commit()
    db.refresh(configuracion)
    
    return configuracion
