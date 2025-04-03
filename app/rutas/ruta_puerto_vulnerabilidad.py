from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.esquemas.puerto_vulnerabilidad_esquemas import PuertoVulnerabilidadCrear
from app.servicios.puerto_vulnerabilidad_servicio import (
    asignar_vulnerabilidad_a_puerto,
    listar_vulnerabilidades_por_puerto
)

router = APIRouter(
    prefix="/puerto_vulnerabilidad",
    tags=["Puerto-Vulnerabilidad"]
)

@router.post("/asignar")
def asignar_vulnerabilidad(datos: PuertoVulnerabilidadCrear, db: Session = Depends(obtener_bd)):
    resultado = asignar_vulnerabilidad_a_puerto(datos, db)
    return {"message": "Vulnerabilidad asignada correctamente", "data": resultado}

@router.get("/listar_por_puerto/{puerto_id}")
def obtener_vulnerabilidades_de_puerto(puerto_id: int, db: Session = Depends(obtener_bd)):
    resultado = listar_vulnerabilidades_por_puerto(puerto_id, db)
    return {"message": "Vulnerabilidades asociadas", "data": resultado}
