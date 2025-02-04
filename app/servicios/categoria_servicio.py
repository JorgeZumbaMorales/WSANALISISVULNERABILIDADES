from sqlalchemy.orm import Session
from app.modelos.categoria import Categoria
from app.esquemas.categoria_esquemas import CategoriaCrear, CategoriaActualizar
from app.core.respuestas import excepcion_no_encontrado, respuesta_exitosa

def crear_categoria(datos_categoria: CategoriaCrear, db: Session):
    nueva_categoria = Categoria(
        nombre_categoria=datos_categoria.nombre_categoria,
        descripcion=datos_categoria.descripcion
    )
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria

def listar_categorias(db: Session):
    return db.query(Categoria).all()

def actualizar_categoria(categoria_id: int, datos_categoria: CategoriaActualizar, db: Session):
    categoria = db.query(Categoria).filter(Categoria.categoria_id == categoria_id).first()
    if not categoria:
        excepcion_no_encontrado("Categoría")

    for key, value in datos_categoria.dict(exclude_unset=True).items():
        setattr(categoria, key, value)

    db.commit()
    db.refresh(categoria)
    return categoria

def actualizar_estado_categoria(categoria_id: int, estado: bool, db: Session):
    categoria = db.query(Categoria).filter(Categoria.categoria_id == categoria_id).first()
    if not categoria:
        excepcion_no_encontrado("Categoría")

    categoria.estado = estado
    db.commit()
    db.refresh(categoria)
    return categoria

def eliminar_categoria(categoria_id: int, db: Session):
    categoria = db.query(Categoria).filter(Categoria.categoria_id == categoria_id).first()
    if not categoria:
        excepcion_no_encontrado("Categoría")

    db.delete(categoria)
    db.commit()
    return respuesta_exitosa("Categoría eliminada exitosamente")
