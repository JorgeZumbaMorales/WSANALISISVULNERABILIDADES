from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.esquemas.puerto_abierto_esquemas import PuertoAbiertoCrear, PuertoAbiertoActualizar
from app.servicios.puerto_abierto_servicio import (
    crear_puerto_abierto, listar_puertos_abiertos, actualizar_puerto_abierto, eliminar_puerto_abierto
)

router = APIRouter(
    prefix="/puertos_abiertos",
    tags=["Puertos Abiertos"]
)

@router.post("/crear_puerto")
def crear_puerto_endpoint(datos_puerto: PuertoAbiertoCrear, db: Session = Depends(obtener_bd)):
    resultado = crear_puerto_abierto(datos_puerto, db)
    return {"message": "Puerto abierto creado correctamente", "data": resultado}

@router.get("/listar_puertos")
def listar_puertos_endpoint(db: Session = Depends(obtener_bd)):
    puertos = listar_puertos_abiertos(db)
    return {"message": "Lista de puertos obtenida exitosamente", "data": puertos}

@router.put("/actualizar_puerto/{puerto_id}")
def actualizar_puerto_endpoint(puerto_id: int, datos_puerto: PuertoAbiertoActualizar, db: Session = Depends(obtener_bd)):
    puerto = actualizar_puerto_abierto(puerto_id, datos_puerto, db)
    if not puerto:
        raise HTTPException(status_code=404, detail="Puerto no encontrado")
    return {"message": "Puerto actualizado exitosamente", "data": puerto}

@router.delete("/eliminar_puerto/{puerto_id}")
def eliminar_puerto_endpoint(puerto_id: int, db: Session = Depends(obtener_bd)):
    eliminar_puerto_abierto(puerto_id, db)
    return {"message": "Puerto eliminado exitosamente"}
