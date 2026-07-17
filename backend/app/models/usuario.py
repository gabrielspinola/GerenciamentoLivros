from datetime import date

from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Usuario(BaseModel):
    idusuario: Optional[int] = None
    nome: str = Field(..., min_length=1, max_length=60)
    login: str = Field(..., min_length=1, max_length=20)
    password: str = Field(..., min_length=5, max_length=200)
    dataAniversario: date #= Field(..., pattern=r'^\d{4}  -\d{2}-\d{2}$')
    ativo: str #= Field(..., pattern=r'^[SN]$')
    email: str = Field(..., format="email")
    ativo_raw: str = ""
    
    #@field_validator('ativo')
    #@classmethod
    #def validar_ativo(cls, v: str) -> str:
    #    v = v.upper()
    #    if v not in ('S', 'N'):
    #        raise ValueError('ativo deve ser S ou N')
    #    return v