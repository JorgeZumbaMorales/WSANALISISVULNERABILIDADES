from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.core.respuestas import respuesta_exitosa, excepcion_no_encontrado
from app.esquemas.tipos_escaneo_esquemas import (
    TiposEscaneoCrear,
    TiposEscaneoActualizar
)
from app.servicios.tipos_escaneo_servicio import (
    crear_tipo_escaneo,
    obtener_tipo_escaneo,
    actualizar_tipo_escaneo,
    eliminar_tipo_escaneo,
    listar_tipos_escaneo
)

router = APIRouter(
    prefix="/tipos_escaneo",
    tags=["Tipos de Escaneo"]
)

@router.post("/crear")
def crear_tipo_escaneo_endpoint(datos: TiposEscaneoCrear, db: Session = Depends(obtener_bd)):
    resultado = crear_tipo_escaneo(datos, db)
    return respuesta_exitosa("Tipo de escaneo creado exitosamente", resultado)

@router.get("/listar")
def listar_tipos_escaneo_endpoint(db: Session = Depends(obtener_bd)):
    tipos = listar_tipos_escaneo(db)
    return respuesta_exitosa("Lista de tipos de escaneo obtenida", tipos)

@router.get("/{tipo_escaneo_id}")
def obtener_tipo_escaneo_endpoint(tipo_escaneo_id: int, db: Session = Depends(obtener_bd)):
    tipo = obtener_tipo_escaneo(db, tipo_escaneo_id)
    if not tipo:
        excepcion_no_encontrado("Tipo de Escaneo")
    return respuesta_exitosa("Tipo de escaneo encontrado", tipo)

@router.put("/actualizar/{tipo_escaneo_id}")
def actualizar_tipo_escaneo_endpoint(tipo_escaneo_id: int, datos: TiposEscaneoActualizar, db: Session = Depends(obtener_bd)):
    resultado = actualizar_tipo_escaneo(tipo_escaneo_id, datos, db)
    return respuesta_exitosa("Tipo de escaneo actualizado correctamente", resultado)

@router.delete("/eliminar/{tipo_escaneo_id}")
def eliminar_tipo_escaneo_endpoint(tipo_escaneo_id: int, db: Session = Depends(obtener_bd)):
    eliminar_tipo_escaneo(tipo_escaneo_id, db)
    return respuesta_exitosa("Tipo de escaneo eliminado exitosamente")
