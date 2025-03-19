from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.servicios.generar_recomendaciones_servicio import (
    generar_recomendacion_por_puerto,
    generar_recomendaciones_por_dispositivo,
    generar_recomendaciones_por_puertos_seleccionados
)

router = APIRouter(
    prefix="/recomendaciones",
    tags=["Recomendaciones"]
)
class PuertosSeleccionadosRequest(BaseModel):
    puertos_ids: List[int]


@router.post("/generar_por_puerto/{puerto_id}")
def generar_recomendacion_puerto_endpoint(puerto_id: int, db: Session = Depends(obtener_bd)):
    """
    📌 Genera una recomendación **para un solo puerto** identificado por `puerto_id`.
    """
    try:
        resultado = generar_recomendacion_por_puerto(db, puerto_id)
        return {"message": "Recomendación generada correctamente", "data": resultado}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.post("/generar_por_dispositivo/{dispositivo_id}")
def generar_recomendaciones_dispositivo_endpoint(dispositivo_id: int, db: Session = Depends(obtener_bd)):
    """
    📌 Genera **recomendaciones para todos los puertos abiertos** de un dispositivo.
    """
    try:
        resultado = generar_recomendaciones_por_dispositivo(db, dispositivo_id)
        return {"message": "Recomendaciones generadas correctamente", "data": resultado}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    
@router.post("/generar_por_puertos_seleccionados")
def generar_recomendaciones_puertos_seleccionados_endpoint(
    request: PuertosSeleccionadosRequest,
    db: Session = Depends(obtener_bd)
):
    """
    📌 Genera recomendaciones solo para los puertos seleccionados.
    """
    try:
        resultado = generar_recomendaciones_por_puertos_seleccionados(db, request.puertos_ids)
        return {"message": "Recomendaciones generadas correctamente", "data": resultado}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

