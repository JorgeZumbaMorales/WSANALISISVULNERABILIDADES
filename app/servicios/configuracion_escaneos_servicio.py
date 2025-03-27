from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.configuracion_escaneo import ConfiguracionEscaneo
from app.esquemas.configuracion_escaneos_esquemas import ConfiguracionEscaneoCrear, ConfiguracionEscaneoActualizar
from sqlalchemy.orm import joinedload
from app.modelos.configuracion_horas_escaneo import ConfiguracionHorasEscaneo
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

def obtener_configuracion_escaneo_con_horas(db: Session):
    """
    📌 Obtiene la configuración de escaneo activa con sus horas asociadas.
    """
    configuracion = db.query(ConfiguracionEscaneo).filter(
        ConfiguracionEscaneo.estado == True
    ).options(
        joinedload(ConfiguracionEscaneo.horas_escaneo)  # ✅ Cargar horas asociadas
    ).first()  # ❌ Aquí faltaba .first()

    if not configuracion:
        print("[ERROR] ❌ No se encontró una configuración activa.")
        return None

    print(f"[INFO] ✅ Configuración activa encontrada: {configuracion.nombre_configuracion_escaneo}")
    return configuracion

# 📌 Listar configuraciones de frecuencia
def listar_configuraciones_frecuencia(db: Session):
    """
    📌 Devuelve solo las configuraciones con frecuencia (frecuencia_minutos no es NULL),
    filtrando solo los datos esenciales.
    """
    configuraciones = db.query(ConfiguracionEscaneo).filter(
        ConfiguracionEscaneo.frecuencia_minutos.isnot(None)
    ).order_by(ConfiguracionEscaneo.fecha_creacion.desc()).all()

    # Convertir resultado en formato JSON
    return [
        {
            "id": config.configuracion_escaneo_id,
            "nombre": config.nombre_configuracion_escaneo,
            "estado": config.estado,
            "frecuencia_minutos": config.frecuencia_minutos,
            "fecha_inicio": config.fecha_inicio,
            "fecha_fin": config.fecha_fin
        }
        for config in configuraciones
    ]


# 📌 Listar configuraciones por horas
def listar_configuraciones_horas(db: Session):
    """
    📌 Devuelve solo las configuraciones con horas programadas, con la lista de horas en un array.
    """
    configuraciones = db.query(ConfiguracionEscaneo).options(
        joinedload(ConfiguracionEscaneo.horas_escaneo)  # ✅ Ahora sí, porque obtenemos el objeto completo
    ).filter(
        ConfiguracionEscaneo.horas_escaneo.any()  # ✅ Filtramos solo configuraciones con horas programadas
    ).distinct().order_by(ConfiguracionEscaneo.fecha_creacion.desc()).all()

    # Convertir resultado en formato JSON
    return [
        {
            "id": config.configuracion_escaneo_id,
            "nombre": config.nombre_configuracion_escaneo,
            "estado": config.estado,
            "fecha_inicio": config.fecha_inicio,
            "fecha_fin": config.fecha_fin,
            "horas": [hora.hora for hora in config.horas_escaneo]  # Extraer solo las horas
        }
        for config in configuraciones
    ]
