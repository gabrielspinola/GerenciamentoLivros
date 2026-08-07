from pydantic import BaseModel, model_validator
from typing import Optional

class LivroModel(BaseModel):
    idlivro: Optional[int] = None
    titulo: str = ""
    autor: str = ""
    ano_publicacao: int = 0
    genero: str = ""
    bloqueado: str = "N"  # "N" para disponível, "S" para bloqueado

    @model_validator(mode="after")
    def Valida(self) -> "LivroModel":
        return self
    
class LivroModelVazio():
    idlivro: int
    titulo: str
    autor: str
    ano_publicacao: str
    genero: str
    bloqueado: str     