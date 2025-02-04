from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.tipo_reporte_esquemas import (
    TipoReporteCrear,
    TipoReporteActualizar,
    TipoReporteActualizarEstado,
)
from app.servicios.tipo_reporte_servicio import (
    crear_tipo_reporte,
    listar_tipos_reporte,
    actualizar_tipo_reporte,
    actualizar_estado_tipo_reporte,
    eliminar_tipo_reporte,
)

router = APIRouter(
    prefix="/tipos_reporte",
    tags=["Tipos de Reporte"]
)

@router.post("/crear_tipo_reporte")
def crear_tipo_reporte_endpoint(datos: TipoReporteCrear, db: Session = Depends(obtener_bd)):
    tipo_reporte = crear_tipo_reporte(datos, db)
    return respuesta_exitosa("Tipo de reporte creado exitosamente", tipo_reporte)

@router.get("/listar_tipos_reporte")
def listar_tipos_reporte_endpoint(db: Session = Depends(obtener_bd)):
    tipos_reporte = listar_tipos_reporte(db)
    return respuesta_exitosa("Lista de tipos de reporte obtenida exitosamente", tipos_reporte)

@router.put("/actualizar_tipo_reporte/{tipo_reporte_id}")
def actualizar_tipo_reporte_endpoint(tipo_reporte_id: int, datos: TipoReporteActualizar, db: Session = Depends(obtener_bd)):
    tipo_reporte = actualizar_tipo_reporte(tipo_reporte_id, datos, db)
    return respuesta_exitosa("Tipo de reporte actualizado exitosamente", tipo_reporte)

@router.put("/actualizar_estado_tipo_reporte/{tipo_reporte_id}")
def actualizar_estado_tipo_reporte_endpoint(tipo_reporte_id: int, datos: TipoReporteActualizarEstado, db: Session = Depends(obtener_bd)):
    tipo_reporte = actualizar_estado_tipo_reporte(tipo_reporte_id, datos, db)
    return respuesta_exitosa("Estado del tipo de reporte actualizado exitosamente", tipo_reporte)

@router.delete("/eliminar_tipo_reporte/{tipo_reporte_id}")
def eliminar_tipo_reporte_endpoint(tipo_reporte_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_tipo_reporte(tipo_reporte_id, db)
