from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class Usuario(BaseModel):
    id: str = Field(..., example='u1')
    nombre: str= Field(..., example='Juan')
    email: EmailStr = Field(..., example='juan.perez@example.com')
    edad: int = Field(..., example=25)


class Proyecto(BaseModel):
    id: str = Field(..., example='p1')
    nombre: str = Field(..., example='Proyecto API CosmosDB 2024')
    descripcion: Optional[str] = Field(None, example='Proyecto para Evaluar conocimiento de CosmosDB')
    id_usuario: str = Field(..., example='u1')
    fecha_creacion: str = Field(..., example='2024-10-31T19:00:00Z')