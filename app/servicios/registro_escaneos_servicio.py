from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modelos.registro_escaneos import RegistroEscaneos
from app.esquemas.registro_escaneos_esquemas import (
    RegistroEscaneoCrear, RegistroEscaneoActualizarEstado
)
from datetime import datetime

# 📌 Crear un nuevo registro de escaneo
def crear_registro_escaneo(configuracion_escaneo_id: int, db: Session):
    nuevo_registro = RegistroEscaneos(
        configuracion_escaneo_id=configuracion_escaneo_id,
        fecha_creacion=datetime.now(),
        estado=True
    )
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    return nuevo_registro

# 📌 Obtener un registro de escaneo por ID
def obtener_registro_escaneo(registro_escaneo_id: int, db: Session):
    registro = db.query(RegistroEscaneos).filter(RegistroEscaneos.registro_escaneo_id == registro_escaneo_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro de escaneo no encontrado")
    return registro

# 📌 Listar todos los registros de escaneos
def listar_registros_escaneos(db: Session):
    return db.query(RegistroEscaneos).order_by(RegistroEscaneos.fecha_creacion.desc()).all()

# 📌 Activar / Desactivar un registro de escaneo
def actualizar_estado_registro_escaneo(registro_escaneo_id: int, datos: RegistroEscaneoActualizarEstado, db: Session):
    registro = db.query(RegistroEscaneos).filter(RegistroEscaneos.registro_escaneo_id == registro_escaneo_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro de escaneo no encontrado")

    registro.estado = datos.estado
    db.commit()
    db.refresh(registro)
    return registro
