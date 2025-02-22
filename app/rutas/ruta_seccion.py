from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa
from app.esquemas.seccion_esquemas import SeccionCrear, SeccionActualizar, SeccionActualizarEstado
from app.servicios.seccion_servicio import crear_seccion, listar_secciones, actualizar_seccion, actualizar_estado_seccion, eliminar_seccion

router = APIRouter(
    prefix="/secciones",
    tags=["Secciones"]
)

# 📌 Crear sección
@router.post("/crear_seccion")
def crear_seccion_endpoint(datos_seccion: SeccionCrear, db: Session = Depends(obtener_bd)):
    seccion = crear_seccion(datos_seccion, db)
    return respuesta_exitosa("Sección creada exitosamente", seccion)

# 📌 Listar secciones
@router.get("/listar_secciones")
def listar_secciones_endpoint(db: Session = Depends(obtener_bd)):
    secciones = listar_secciones(db)
    return respuesta_exitosa("Lista de secciones obtenida exitosamente", secciones)

# 📌 Actualizar sección
@router.put("/actualizar_seccion/{seccion_id}")
def actualizar_seccion_endpoint(seccion_id: int, datos_seccion: SeccionActualizar, db: Session = Depends(obtener_bd)):
    seccion = actualizar_seccion(seccion_id, datos_seccion, db)
    if not seccion:
        excepcion_no_encontrado("Sección")
    return respuesta_exitosa("Sección actualizada exitosamente", seccion)

# 📌 Actualizar estado de una sección
@router.put("/actualizar_estado_seccion/{seccion_id}")
def actualizar_estado_seccion_endpoint(seccion_id: int, datos_estado: SeccionActualizarEstado, db: Session = Depends(obtener_bd)):
    seccion = actualizar_estado_seccion(seccion_id, datos_estado, db)
    if not seccion:
        excepcion_no_encontrado("Sección")
    return respuesta_exitosa("Estado de la sección actualizado exitosamente", seccion)

# 📌 Eliminar sección
@router.delete("/eliminar_seccion/{seccion_id}")
def eliminar_seccion_endpoint(seccion_id: int, db: Session = Depends(obtener_bd)):
    eliminar_seccion(seccion_id, db)
    return respuesta_exitosa("Sección eliminada exitosamente")
