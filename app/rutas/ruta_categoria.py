from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.categoria_esquemas import (
    CategoriaCrear,
    CategoriaActualizar,
    CategoriaActualizarEstado
)
from app.servicios.categoria_servicio import (
    crear_categoria,
    listar_categorias,
    actualizar_categoria,
    actualizar_estado_categoria,
    eliminar_categoria
)

router = APIRouter(
    prefix="/categorias",
    tags=["Categorías"]
)

@router.post("/crear_categoria")
def crear_categoria_endpoint(datos_categoria: CategoriaCrear, db: Session = Depends(obtener_bd)):
    categoria = crear_categoria(datos_categoria, db)
    return respuesta_exitosa("Categoría creada exitosamente", categoria)

@router.get("/listar_categorias")
def listar_categorias_endpoint(db: Session = Depends(obtener_bd)):
    categorias = listar_categorias(db)
    return respuesta_exitosa("Lista de categorías obtenida exitosamente", categorias)

@router.put("/actualizar_categoria/{categoria_id}")
def actualizar_categoria_endpoint(categoria_id: int, datos_categoria: CategoriaActualizar, db: Session = Depends(obtener_bd)):
    categoria = actualizar_categoria(categoria_id, datos_categoria, db)
    return respuesta_exitosa("Categoría actualizada exitosamente", categoria)

@router.put("/actualizar_estado_categoria/{categoria_id}")
def actualizar_estado_categoria_endpoint(categoria_id: int, datos_estado: CategoriaActualizarEstado, db: Session = Depends(obtener_bd)):
    categoria = actualizar_estado_categoria(categoria_id, datos_estado.estado, db)
    return respuesta_exitosa("Estado de la categoría actualizado exitosamente", categoria)

@router.delete("/eliminar_categoria/{categoria_id}")
def eliminar_categoria_endpoint(categoria_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_categoria(categoria_id, db)
