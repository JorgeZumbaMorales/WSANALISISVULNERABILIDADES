from sqlalchemy.orm import Session
from app.modelos.dispositivo_categoria import DispositivoCategoria
from app.esquemas.dispositivo_categoria_esquemas import DispositivoCategoriaCrear
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_dispositivo_categoria(datos: DispositivoCategoriaCrear, db: Session):
    nueva_relacion = DispositivoCategoria(
        dispositivo_id=datos.dispositivo_id,
        categoria_id=datos.categoria_id
    )
    db.add(nueva_relacion)
    db.commit()
    db.refresh(nueva_relacion)
    return nueva_relacion

def listar_dispositivo_categorias(db: Session):
    return db.query(DispositivoCategoria).all()

def actualizar_estado_dispositivo_categoria(relacion_id: int, estado: bool, db: Session):
    relacion = db.query(DispositivoCategoria).filter(DispositivoCategoria.dispositivo_categoria_id == relacion_id).first()
    if not relacion:
        excepcion_no_encontrado("Relación dispositivo-categoría")

    relacion.estado = estado
    db.commit()
    db.refresh(relacion)
    return relacion

def eliminar_dispositivo_categoria(relacion_id: int, db: Session):
    relacion = db.query(DispositivoCategoria).filter(DispositivoCategoria.dispositivo_categoria_id == relacion_id).first()
    if not relacion:
        excepcion_no_encontrado("Relación dispositivo-categoría")

    db.delete(relacion)
    db.commit()
    return respuesta_exitosa("Relación dispositivo-categoría eliminada exitosamente")
