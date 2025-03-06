from datetime import datetime, timedelta
from jose import jwt
from app.config.configuracion import CLAVE_SECRETA, ALGORITMO, TIEMPO_EXPIRACION_TOKEN_MINUTOS

def generar_token_jwt(datos: dict):
    """Genera un JWT con datos del usuario y tiempo de expiración."""
    datos_copia = datos.copy()
    expira = datetime.utcnow() + timedelta(minutes=TIEMPO_EXPIRACION_TOKEN_MINUTOS)
    datos_copia.update({"exp": expira})
    return jwt.encode(datos_copia, CLAVE_SECRETA, algorithm=ALGORITMO)
