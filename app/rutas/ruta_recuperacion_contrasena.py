from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd  # Asegúrate de importar la función para obtener la BD
from app.servicios.recuperacion_contrasena_servicio import RecuperacionServicio
from app.esquemas.codigo_recuperacion_esquema import ValidarCodigoRecuperacion
router = APIRouter(prefix="/recuperacion", tags=["Recuperación de Contraseña"])

# 📌 Esquema de entrada con Pydantic
class SolicitudRecuperacion(BaseModel):
    usuario_id: int
    correo: str
    usuario: str

@router.post("/solicitar")
def solicitar_codigo(datos: SolicitudRecuperacion, db: Session = Depends(obtener_bd)):
    """Ruta para solicitar un código de recuperación de contraseña."""
    respuesta = RecuperacionServicio.enviar_codigo_recuperacion(db, datos.usuario_id, datos.correo, datos.usuario)

    if respuesta["estado"] == "error":
        raise HTTPException(status_code=400, detail=respuesta["mensaje"])

    return {"mensaje": "Código de recuperación enviado correctamente."}

@router.post("/validar_codigo")
def validar_codigo_endpoint(datos: ValidarCodigoRecuperacion, db: Session = Depends(obtener_bd)):
    """Ruta para validar si un código OTP es correcto y está activo."""
    resultado = RecuperacionServicio.validar_codigo(db, datos.usuario, datos.codigo)

    if resultado["estado"] == "error":
        raise HTTPException(status_code=400, detail=resultado["mensaje"])

    return {"mensaje": "Código válido."}