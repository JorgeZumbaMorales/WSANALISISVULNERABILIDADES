from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.configuracion_horas_escaneo import ConfiguracionHorasEscaneo
from app.esquemas.configuracion_horas_escaneo_esquemas import ConfiguracionHorasEscaneoCrear, ConfiguracionHorasEscaneoActualizar

# 📌 Crear una nueva hora de escaneo
def crear_hora_escaneo(datos: ConfiguracionHorasEscaneoCrear, db: Session):
    nueva_hora = ConfiguracionHorasEscaneo(
        configuracion_escaneo_id=datos.configuracion_escaneo_id,
        hora=datos.hora
    )

    db.add(nueva_hora)
    db.commit()
    db.refresh(nueva_hora)
    return nueva_hora

# 📌 Obtener una hora de escaneo por ID
def obtener_hora_escaneo(id: int, db: Session):
    hora = db.query(ConfiguracionHorasEscaneo).filter(
        ConfiguracionHorasEscaneo.id == id
    ).first()

    if not hora:
        raise HTTPException(status_code=404, detail="Hora de escaneo no encontrada")

    return hora

# 📌 Actualizar una hora de escaneo
def actualizar_hora_escaneo(id: int, datos: ConfiguracionHorasEscaneoActualizar, db: Session):
    hora = db.query(ConfiguracionHorasEscaneo).filter(
        ConfiguracionHorasEscaneo.id == id
    ).first()

    if not hora:
        raise HTTPException(status_code=404, detail="Hora de escaneo no encontrada")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(hora, key, value)

    db.commit()
    db.refresh(hora)
    return hora

# 📌 Listar todas las horas de escaneo para una configuración específica
def listar_horas_escaneo(configuracion_escaneo_id: int, db: Session):
    return db.query(ConfiguracionHorasEscaneo).filter(
        ConfiguracionHorasEscaneo.configuracion_escaneo_id == configuracion_escaneo_id
    ).order_by(ConfiguracionHorasEscaneo.hora.asc()).all()

# 📌 Eliminar una hora de escaneo
def eliminar_hora_escaneo(id: int, db: Session):
    hora = db.query(ConfiguracionHorasEscaneo).filter(
        ConfiguracionHorasEscaneo.id == id
    ).first()

    if not hora:
        raise HTTPException(status_code=404, detail="Hora de escaneo no encontrada")
    
    db.delete(hora)
    db.commit()
    return {"mensaje": "Hora de escaneo eliminada exitosamente"}
