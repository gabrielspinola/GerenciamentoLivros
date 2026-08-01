from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Settings(BaseModel):
    idsettings: Optional[int] = None
    diasLivroEmprestado: int = Field(..., ge=0)

    @field_validator('diasLivroEmprestado')
    @classmethod
    def validate_diasLivroEmprestado(cls, v):
        if v < 0:
            raise ValueError('diasLivroEmprestado deve ser um número inteiro não negativo')
        return v