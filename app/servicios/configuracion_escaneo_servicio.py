from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.modelos.configuracion_escaneo import ConfiguracionEscaneo
from app.esquemas.configuracion_escaneo_esquemas import ConfiguracionEscaneoCrear, ConfiguracionEscaneoActualizar

def crear_configuracion_escaneo(datos: ConfiguracionEscaneoCrear, db: Session):
    """
    Crea una nueva configuración de escaneo.
    """
    try:
        nueva_configuracion = ConfiguracionEscaneo(
            tipo_escaneo_id=datos.tipo_escaneo_id,
            frecuencia_minutos=datos.frecuencia_minutos,
            hora_especifica=datos.hora_especifica,
            estado=datos.estado
        )

        db.add(nueva_configuracion)
        db.commit()
        db.refresh(nueva_configuracion)
        return nueva_configuracion

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error en la base de datos: {str(e)}")

def actualizar_configuracion_escaneo(configuracion_id: int, datos: ConfiguracionEscaneoActualizar, db: Session):
    """
    Actualiza una configuración de escaneo existente.
    """
    configuracion = db.query(ConfiguracionEscaneo).filter(ConfiguracionEscaneo.configuracion_escaneo_id == configuracion_id).first()
    
    if not configuracion:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")

    if datos.frecuencia_minutos:
        configuracion.frecuencia_minutos = datos.frecuencia_minutos
    if datos.hora_especifica:
        configuracion.hora_especifica = datos.hora_especifica
    if datos.estado is not None:
        configuracion.estado = datos.estado

    db.commit()
    db.refresh(configuracion)
    return configuracion

def eliminar_configuracion_escaneo(configuracion_id: int, db: Session):
    """
    Elimina una configuración de escaneo.
    """
    configuracion = db.query(ConfiguracionEscaneo).filter(ConfiguracionEscaneo.configuracion_escaneo_id == configuracion_id).first()
    
    if not configuracion:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    
    db.delete(configuracion)
    db.commit()
    return {"message": "Configuración eliminada exitosamente"}

def obtener_configuracion_actual(db: Session):
    """
    Obtiene la configuración activa más reciente.
    """
    return db.query(ConfiguracionEscaneo).filter(ConfiguracionEscaneo.estado == True).order_by(ConfiguracionEscaneo.fecha_creacion.desc()).first()

def listar_configuraciones(db: Session):
    """
    Lista todas las configuraciones registradas.
    """
    return db.query(ConfiguracionEscaneo).all()
