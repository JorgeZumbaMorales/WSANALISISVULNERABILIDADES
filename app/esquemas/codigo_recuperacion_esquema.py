from pydantic import BaseModel, Field

class ValidarCodigoRecuperacion(BaseModel):
    usuario: str
    codigo: str = Field(..., min_length=6, max_length=6, example="123456")
