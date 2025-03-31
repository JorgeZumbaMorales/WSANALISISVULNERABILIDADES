from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.transacciones.transaccion_dispositivo_sistema_operativo import transaccion_actualizar_dispositivo_con_so,transaccion_eliminar_dispositivo_completo
from app.esquemas.dispositivo_esquemas import (
    DispositivoCrear, 
    DispositivoActualizar,
    DispositivoActualizarEstado,
    DispositivoActualizarConSO
)
from app.servicios.dispositivo_servicio import (
    crear_dispositivo,
    listar_dispositivos,
    listar_dispositivos_completo,
    actualizar_dispositivo,
    eliminar_dispositivo,
    listar_todos_los_dispositivos_completo,
    listar_dispositivos_por_riesgo,
    actualizar_estado_dispositivo
)

router = APIRouter(
    prefix="/dispositivos",
    tags=["Dispositivos"]
)

@router.post("/crear_dispositivo")
def crear_dispositivo_endpoint(datos_dispositivo: DispositivoCrear, db: Session = Depends(obtener_bd)):
    dispositivo = crear_dispositivo(datos_dispositivo, db)
    return {"message": "Dispositivo creado exitosamente", "data": dispositivo}

@router.get("/listar_dispositivos")
def listar_dispositivos_endpoint(db: Session = Depends(obtener_bd)):
    dispositivos = listar_dispositivos(db)
    return {"message": "Lista de dispositivos obtenida exitosamente", "data": dispositivos}

@router.get("/listar_dispositivos_completo")
def listar_dispositivos_completo_endpoint(db: Session = Depends(obtener_bd)):
    dispositivos = listar_dispositivos_completo(db)
    return {"message": "Lista de dispositivos obtenida exitosamente", "data": dispositivos}

@router.get("/listar_todos_los_dispositivos_completo")
def listar_todos_los_dispositivos_completo_endpoint(db: Session = Depends(obtener_bd)):
    dispositivos = listar_todos_los_dispositivos_completo(db)
    return {"message": "Lista completa de dispositivos obtenida exitosamente", "data": dispositivos}

@router.put("/actualizar_dispositivo/{dispositivo_id}")
def actualizar_dispositivo_endpoint(dispositivo_id: int, datos_dispositivo: DispositivoActualizarConSO, db: Session = Depends(obtener_bd)):
    dispositivo_actualizado = transaccion_actualizar_dispositivo_con_so(dispositivo_id, datos_dispositivo, db)
    
    if not dispositivo_actualizado:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    return {
        "message": "Dispositivo actualizado exitosamente",
        "data": dispositivo_actualizado
    }

@router.delete("/eliminar_dispositivo/{dispositivo_id}")
def eliminar_dispositivo_endpoint(dispositivo_id: int, db: Session = Depends(obtener_bd)):
    return transaccion_eliminar_dispositivo_completo(dispositivo_id, db)


@router.get("/riesgo/{nivel_riesgo}")
def listar_dispositivos_riesgo_endpoint(nivel_riesgo: str, db: Session = Depends(obtener_bd)):
    dispositivos = listar_dispositivos_por_riesgo(db, nivel_riesgo)
    return {"message": f"Lista de dispositivos con riesgo {nivel_riesgo}", "data": dispositivos}

@router.put("/actualizar_estado_dispositivo/{dispositivo_id}")
def actualizar_estado_dispositivo_endpoint(dispositivo_id: int, datos_estado: DispositivoActualizarEstado, db: Session = Depends(obtener_bd)):
    """
    📌 Ruta para actualizar el estado de un dispositivo específico.
    """
    dispositivo_actualizado = actualizar_estado_dispositivo(dispositivo_id, datos_estado, db)
    return {"message": f"Estado del dispositivo {dispositivo_id} actualizado exitosamente", "data": dispositivo_actualizado}
