from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.servicios.correo_servicio import ServicioCorreo

# 📌 Esquema de datos para la API
class CorreoSchema(BaseModel):
    destinatarios: list[str]
    asunto: str
    mensaje: str
    es_html: bool = False  # Opcional, por defecto es texto plano

router = APIRouter(prefix="/correo", tags=["Correos"])

@router.post("/enviar")
def enviar_correo(datos: CorreoSchema):
    respuesta = ServicioCorreo.enviar_correo(
        destinatarios=datos.destinatarios,
        asunto=datos.asunto,
        mensaje=datos.mensaje,
        es_html=datos.es_html
    )

    if respuesta["estado"] == "error":
        raise HTTPException(status_code=400, detail=respuesta["mensaje"])

    return respuesta
