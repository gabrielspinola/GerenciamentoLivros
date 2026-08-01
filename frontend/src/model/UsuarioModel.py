from datetime import date
from pydantic import BaseModel, model_validator
from typing import Optional

class UsuarioModel(BaseModel):
    idusuario: Optional[int] = None
    nome: str 
    login: str 
    password: str
    dataAniversario: date
    dataAniversario_raw: str = ""
    ativo: str
    email: str
    ativo_raw: str = ""

    @model_validator(mode="after")
    def calcular_campos_raw(self) -> "UsuarioModel":
        self.dataAniversario_raw = self.dataAniversario.strftime("%d/%m/%Y")
        self.ativo_raw = "ATIVO" if self.ativo == "A" else "INATIVO"
        return self

class UsuarioModelVazio():
    idusuario: int
    nome: str 
    login: str 
    password: str
    dataAniversario: date
    ativo: str
    email: str
    