from pydantic import BaseModel, Field

# Esquema para crear una relación dispositivo-categoría
class DispositivoCategoriaCrear(BaseModel):
    dispositivo_id: int = Field(..., example=1)
    categoria_id: int = Field(..., example=2)

# Esquema para actualizar el estado de una relación dispositivo-categoría
class DispositivoCategoriaActualizarEstado(BaseModel):
    estado: bool = Field(..., example=True)
