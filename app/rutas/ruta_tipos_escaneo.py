from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.servicios.tipos_escaneo_servicio import (
    crear_tipo_escaneo, 
    actualizar_tipo_escaneo, 
    eliminar_tipo_escaneo,
    obtener_tipo_escaneo,
    listar_tipos_escaneo
)
from app.esquemas.tipos_escaneo_esquemas import TipoEscaneoCrear, TipoEscaneoActualizar

router = APIRouter(
    prefix="/tipos_escaneo",
    tags=["Tipos de Escaneo"]
)

@router.post("/")
def crear_tipo_escaneo_endpoint(datos: TipoEscaneoCrear, db: Session = Depends(obtener_bd)):
    resultado = crear_tipo_escaneo(datos, db)
    return {"message": "Tipo de escaneo creado exitosamente", "data": resultado}

@router.put("/{tipo_escaneo_id}")
def actualizar_tipo_escaneo_endpoint(tipo_escaneo_id: int, datos: TipoEscaneoActualizar, db: Session = Depends(obtener_bd)):
    resultado = actualizar_tipo_escaneo(tipo_escaneo_id, datos, db)
    return {"message": "Tipo de escaneo actualizado", "data": resultado}

@router.delete("/{tipo_escaneo_id}")
def eliminar_tipo_escaneo_endpoint(tipo_escaneo_id: int, db: Session = Depends(obtener_bd)):
    eliminar_tipo_escaneo(tipo_escaneo_id, db)
    return {"message": "Tipo de escaneo eliminado exitosamente"}

@router.get("/{tipo_escaneo_id}")
def obtener_tipo_escaneo_endpoint(tipo_escaneo_id: int, db: Session = Depends(obtener_bd)):
    tipo_escaneo = obtener_tipo_escaneo(tipo_escaneo_id, db)
    return {"message": "Tipo de escaneo encontrado", "data": tipo_escaneo}

@router.get("/")
def listar_tipos_escaneo_endpoint(db: Session = Depends(obtener_bd)):
    tipos = listar_tipos_escaneo(db)
    return {"message": "Lista de tipos de escaneo obtenida", "data": tipos}
