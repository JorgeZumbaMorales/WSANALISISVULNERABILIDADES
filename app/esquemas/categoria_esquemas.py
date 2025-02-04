from pydantic import BaseModel, Field
from typing import Optional

# Esquema para crear una categoría
class CategoriaCrear(BaseModel):
    nombre_categoria: str = Field(..., example="Redes")
    descripcion: Optional[str] = Field(None, example="Categoría de dispositivos de red")

# Esquema para actualizar una categoría
class CategoriaActualizar(BaseModel):
    nombre_categoria: Optional[str] = Field(None, example="Redes Actualizado")
    descripcion: Optional[str] = Field(None, example="Categoría de dispositivos de red actualizada")

# Esquema para actualizar el estado de una categoría
class CategoriaActualizarEstado(BaseModel):
    estado: bool = Field(..., example=True)
