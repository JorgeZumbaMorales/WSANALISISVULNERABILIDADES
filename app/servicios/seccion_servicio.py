from sqlalchemy.orm import Session
from app.modelos.seccion import Seccion
from app.esquemas.seccion_esquemas import SeccionCrear, SeccionActualizar, SeccionActualizarEstado
from fastapi import HTTPException

# 📌 Crear una nueva sección
def crear_seccion(datos_seccion: SeccionCrear, db: Session):
    nueva_seccion = Seccion(
        nombre_seccion=datos_seccion.nombre_seccion,
        descripcion=datos_seccion.descripcion,
        ruta=datos_seccion.ruta,
        icono=datos_seccion.icono
    )
    db.add(nueva_seccion)
    db.commit()
    db.refresh(nueva_seccion)
    return nueva_seccion

# 📌 Listar todas las secciones
def listar_secciones(db: Session):
    return db.query(Seccion).all()

# 📌 Actualizar una sección existente
def actualizar_seccion(seccion_id: int, datos_seccion: SeccionActualizar, db: Session):
    seccion_existente = db.query(Seccion).filter(Seccion.seccion_id == seccion_id).first()
    if not seccion_existente:
        raise HTTPException(status_code=404, detail="Sección no encontrada")

    if datos_seccion.nombre_seccion:
        seccion_existente.nombre_seccion = datos_seccion.nombre_seccion
    if datos_seccion.descripcion:
        seccion_existente.descripcion = datos_seccion.descripcion
    if datos_seccion.ruta:
        seccion_existente.ruta = datos_seccion.ruta
    if datos_seccion.icono:
        seccion_existente.icono = datos_seccion.icono

    db.commit()
    db.refresh(seccion_existente)
    return seccion_existente

# 📌 Actualizar el estado de una sección
def actualizar_estado_seccion(seccion_id: int, datos_estado: SeccionActualizarEstado, db: Session):
    seccion_existente = db.query(Seccion).filter(Seccion.seccion_id == seccion_id).first()
    if not seccion_existente:
        raise HTTPException(status_code=404, detail="Sección no encontrada")

    seccion_existente.estado = datos_estado.estado

    db.commit()
    db.refresh(seccion_existente)
    return seccion_existente

# 📌 Eliminar una sección
def eliminar_seccion(seccion_id: int, db: Session):
    seccion_existente = db.query(Seccion).filter(Seccion.seccion_id == seccion_id).first()
    if not seccion_existente:
        raise HTTPException(status_code=404, detail="Sección no encontrada")

    db.delete(seccion_existente)
    db.commit()
    return {"message": "Sección eliminada exitosamente"}
