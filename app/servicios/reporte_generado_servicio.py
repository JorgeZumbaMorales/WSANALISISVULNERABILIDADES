from sqlalchemy.orm import Session
from app.modelos.reporte_generado import ReporteGenerado
from app.esquemas.reporte_generado_esquemas import (
    ReporteGeneradoCrear,
    ReporteGeneradoActualizar,
    ReporteGeneradoActualizarEstado,
)
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_reporte_generado(datos: ReporteGeneradoCrear, db: Session):
    nuevo_reporte = ReporteGenerado(
        tipo_reporte_id=datos.tipo_reporte_id,
        nombre_reporte_generado=datos.nombre_reporte_generado,
        descripcion=datos.descripcion,
        usuario_id=datos.usuario_id,
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin,
        contenido=datos.contenido
    )
    db.add(nuevo_reporte)
    db.commit()
    db.refresh(nuevo_reporte)
    return nuevo_reporte

def listar_reportes_generados(db: Session):
    return db.query(ReporteGenerado).all()

def actualizar_reporte_generado(reporte_id: int, datos: ReporteGeneradoActualizar, db: Session):
    reporte = db.query(ReporteGenerado).filter(ReporteGenerado.reporte_generado_id == reporte_id).first()
    if not reporte:
        excepcion_no_encontrado("Reporte Generado")

    if datos.nombre_reporte_generado:
        reporte.nombre_reporte_generado = datos.nombre_reporte_generado
    if datos.descripcion:
        reporte.descripcion = datos.descripcion
    if datos.contenido:
        reporte.contenido = datos.contenido

    db.commit()
    db.refresh(reporte)
    return reporte

def actualizar_estado_reporte_generado(reporte_id: int, datos: ReporteGeneradoActualizarEstado, db: Session):
    reporte = db.query(ReporteGenerado).filter(ReporteGenerado.reporte_generado_id == reporte_id).first()
    if not reporte:
        excepcion_no_encontrado("Reporte Generado")

    reporte.estado = datos.estado

    db.commit()
    db.refresh(reporte)
    return reporte

def eliminar_reporte_generado(reporte_id: int, db: Session):
    reporte = db.query(ReporteGenerado).filter(ReporteGenerado.reporte_generado_id == reporte_id).first()
    if not reporte:
        excepcion_no_encontrado("Reporte Generado")

    db.delete(reporte)
    db.commit()
    return {"mensaje": "Reporte generado eliminado exitosamente"}
