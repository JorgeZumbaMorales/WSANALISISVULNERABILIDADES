from sqlalchemy.orm import Session
from app.modelos.tipo_reporte import TipoReporte
from app.esquemas.tipo_reporte_esquemas import TipoReporteCrear, TipoReporteActualizar, TipoReporteActualizarEstado
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_tipo_reporte(datos: TipoReporteCrear, db: Session):
    nuevo_tipo_reporte = TipoReporte(
        nombre_tipo_reporte=datos.nombre_tipo_reporte,
        descripcion=datos.descripcion
    )
    db.add(nuevo_tipo_reporte)
    db.commit()
    db.refresh(nuevo_tipo_reporte)
    return nuevo_tipo_reporte

def listar_tipos_reporte(db: Session):
    return db.query(TipoReporte).all()

def actualizar_tipo_reporte(tipo_reporte_id: int, datos: TipoReporteActualizar, db: Session):
    tipo_reporte = db.query(TipoReporte).filter(TipoReporte.tipo_reporte_id == tipo_reporte_id).first()
    if not tipo_reporte:
        excepcion_no_encontrado("Tipo de Reporte")

    if datos.nombre_tipo_reporte:
        tipo_reporte.nombre_tipo_reporte = datos.nombre_tipo_reporte
    if datos.descripcion:
        tipo_reporte.descripcion = datos.descripcion

    db.commit()
    db.refresh(tipo_reporte)
    return tipo_reporte

def actualizar_estado_tipo_reporte(tipo_reporte_id: int, datos: TipoReporteActualizarEstado, db: Session):
    tipo_reporte = db.query(TipoReporte).filter(TipoReporte.tipo_reporte_id == tipo_reporte_id).first()
    if not tipo_reporte:
        excepcion_no_encontrado("Tipo de Reporte")

    tipo_reporte.estado = datos.estado

    db.commit()
    db.refresh(tipo_reporte)
    return tipo_reporte

def eliminar_tipo_reporte(tipo_reporte_id: int, db: Session):
    tipo_reporte = db.query(TipoReporte).filter(TipoReporte.tipo_reporte_id == tipo_reporte_id).first()
    if not tipo_reporte:
        excepcion_no_encontrado("Tipo de Reporte")

    db.delete(tipo_reporte)
    db.commit()
    return {"mensaje": "Tipo de reporte eliminado exitosamente"}
