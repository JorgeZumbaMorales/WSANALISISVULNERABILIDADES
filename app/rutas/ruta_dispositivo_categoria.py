from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa
from app.esquemas.dispositivo_categoria_esquemas import (
    DispositivoCategoriaCrear,
    DispositivoCategoriaActualizarEstado
)
from app.servicios.dispositivo_categoria_servicio import (
    crear_dispositivo_categoria,
    listar_dispositivo_categorias,
    actualizar_estado_dispositivo_categoria,
    eliminar_dispositivo_categoria
)

router = APIRouter(
    prefix="/dispositivo_categoria",
    tags=["Dispositivo-Categoría"]
)

@router.post("/crear_relacion")
def crear_relacion_endpoint(datos: DispositivoCategoriaCrear, db: Session = Depends(obtener_bd)):
    relacion = crear_dispositivo_categoria(datos, db)
    return respuesta_exitosa("Relación dispositivo-categoría creada exitosamente", relacion)

@router.get("/listar_relaciones")
def listar_relaciones_endpoint(db: Session = Depends(obtener_bd)):
    relaciones = listar_dispositivo_categorias(db)
    return respuesta_exitosa("Lista de relaciones dispositivo-categoría obtenida exitosamente", relaciones)

@router.put("/actualizar_estado/{relacion_id}")
def actualizar_estado_endpoint(relacion_id: int, datos: DispositivoCategoriaActualizarEstado, db: Session = Depends(obtener_bd)):
    relacion = actualizar_estado_dispositivo_categoria(relacion_id, datos.estado, db)
    return respuesta_exitosa("Estado de la relación dispositivo-categoría actualizado exitosamente", relacion)

@router.delete("/eliminar_relacion/{relacion_id}")
def eliminar_relacion_endpoint(relacion_id: int, db: Session = Depends(obtener_bd)):
    return eliminar_dispositivo_categoria(relacion_id, db)
