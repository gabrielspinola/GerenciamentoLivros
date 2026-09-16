from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Livro(BaseModel):
    idlivro: Optional[int] = None
    titulo: str = Field(..., min_length=1, max_length=200)
    autor: str = Field(..., min_length=1, max_length=200)
    ano_publicacao: int = Field(..., ge=1000, le=2100)
    genero: str = Field(..., min_length=1, max_length=100)
    bloqueado: str = Field(..., pattern=r'^[SN]$')
    createAt: Optional[date] = None

    @field_validator('bloqueado')
    @classmethod
    def validar_bloqueado(cls, v: str) -> str:
        v = v.upper()
        if v not in ('S', 'N'):
            raise ValueError('bloqueado deve ser S ou N')
        return v
    
    @field_validator('createAt', mode='before')
    @classmethod
    def truncar_hora(cls, v):
        if isinstance(v, datetime):
            return v.date()
        return v