from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd
from app.esquemas.usuario_esquemas import UsuarioLogin
from app.servicios.usuario_servicio import verificar_credenciales
from app.seguridad.jwt import generar_token_jwt

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

@router.post("/login")
def login(datos: UsuarioLogin, db: Session = Depends(obtener_bd)):
    usuario = verificar_credenciales(db, datos)

    # Generar token JWT
    token = generar_token_jwt({"usuario_id": usuario.usuario_id, "nombre_usuario": usuario.nombre_usuario})

    return {"access_token": token, "token_type": "bearer"}
