from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.base_datos import obtener_bd
from app.esquemas.puerto_abierto_esquemas import PuertoAbiertoCrear, PuertoAbiertoActualizar, PuertosSeleccionadosPeticion
from app.servicios.puerto_abierto_servicio import (
    crear_puerto_abierto, listar_puertos_abiertos, actualizar_puerto_abierto, eliminar_puerto_abierto,
    obtener_recomendaciones_por_puertos
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

@router.post("/ver_recomendaciones")
def obtener_recomendaciones_por_puertos_endpoint(
    request: PuertosSeleccionadosPeticion,
    db: Session = Depends(obtener_bd)
):
    """
    📌 Obtiene recomendaciones solo para los puertos seleccionados.
    """
    try:
        print("[DEBUG] Recibido en el backend:", request.puertos_ids)  # 🔥 Imprime lo recibido
        resultado = obtener_recomendaciones_por_puertos(db, request)
        return {"message": "Consulta exitosa", "data": resultado}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")