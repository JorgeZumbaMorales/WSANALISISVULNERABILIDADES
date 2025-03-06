from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.config.configuracion import CLAVE_SECRETA, ALGORITMO
from app.modelos.usuario import Usuario
from sqlalchemy.orm import Session
from app.core.base_datos import obtener_bd

# Esquema de autenticación con OAuth2 Bearer Token
esquema_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

def obtener_usuario_desde_token(token: str = Depends(esquema_oauth2), db: Session = Depends(obtener_bd)):
    """Valida el token JWT y devuelve el usuario autenticado."""
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        datos_token = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        usuario_id = datos_token.get("usuario_id")

        if not usuario_id:
            raise credenciales_invalidas

        usuario = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
        if not usuario:
            raise credenciales_invalidas

        return usuario  # Retorna el usuario autenticado

    except JWTError:
        raise credenciales_invalidas
