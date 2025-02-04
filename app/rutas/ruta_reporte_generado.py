from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.reporte_generado_esquemas import (
    ReporteGeneradoCrear,
    ReporteGeneradoActualizar,
    ReporteGeneradoActualizarEstado,
)
from app.servicios.reporte_generado_servicio import (
    crear_reporte_generado,
    listar_reportes_generados,
    actualizar_reporte_generado,
    actualizar_estado_reporte_generado,
    eliminar_reporte_generado,
)

router = APIRouter(
    prefix="/reportes_generados",
    tags=["Reportes Generados"]
)

@router.post("/crear_reporte_generado")
def crear_reporte_generado_endpoint(datos: ReporteGeneradoCrear, db: Session = Depends(obtener_bd)):
    reporte = crear_reporte_generado(datos, db)
    return respuesta_exitosa("Reporte generado exitosamente", reporte)

@router.get("/listar_reportes_generados")
def listar_reportes_generados_endpoint(db: Session = Depends(obtener_bd)):
    reportes = listar_reportes_generados(db)
    return respuesta_exitosa("Lista de reportes generados obtenida exitosamente", reportes)

@router.put("/actualizar_reporte_generado/{reporte_id}")
def actualizar_reporte_generado_endpoint(reporte_id: int, datos: ReporteGeneradoActualizar, db: Session = Depends(obtener_bd)):
    reporte = actualizar_reporte_generado(reporte_id, datos, db)
    return respuesta_exitosa("Reporte generado actualizado exitosamente", reporte)

@router.put("/actualizar_estado_reporte_generado/{reporte_id}")
def actualizar_estado_reporte_generado_endpoint(reporte_id: int, datos: ReporteGeneradoActualizarEstado, db: Session = Depends(obtener_bd)):
    reporte = actualizar_estado_reporte_generado(reporte_id, datos, db)
    return respuesta_exitosa("Estado del reporte generado actualizado exitosamente", reporte)

@router.delete("/eliminar_reporte_generado/{reporte_id}")
def eliminar_reporte_generado_endpoint(reporte_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_reporte_generado(reporte_id, db)
