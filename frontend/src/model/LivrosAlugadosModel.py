from datetime import date

from pydantic import BaseModel, model_validator
from typing import Optional

class LivrosAlugadosModel(BaseModel):
    idLivrosAlugados: Optional[int] = None
    idusuario: int = 0
    nome: str = ""
    idlivro: int = 0
    titulo: str = ""
    dataAluguel: date = None
    dataDevolucao: date = None
    dataEntrega: Optional[date]  = None
    dataAluguel_raw: str = ""
    dataDevolucao_raw: str = ""
    dataEntrega_raw: str = ""

    @model_validator(mode="after")
    def Valida(self) -> "LivrosAlugadosModel":
        
        if self.dataAluguel is not None:
            self.dataAluguel_raw = self.dataAluguel.strftime("%d/%m/%Y")
        
        if self.dataDevolucao is not None:
            self.dataDevolucao_raw = self.dataDevolucao.strftime("%d/%m/%Y")
        
        if self.dataEntrega is not None:
            self.dataEntrega_raw = self.dataEntrega.strftime("%d/%m/%Y")
        return self
    
class LivrosAlugadosModelVazio():
    idLivrosAlugados: int
    idusuario: int
    nome: str
    idlivro: int
    titulo: str
    dataAluguel: str
    dataDevolucao: str
    dataEntrega: str