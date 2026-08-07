from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date

class LivrosAlugados(BaseModel):
    idLivrosAlugados: Optional[int] = None
    idusuario: int = Field(..., ge=0)
    nome: Optional[str] = None
    idlivro: int = Field(..., ge=0)
    titulo: Optional[str] = None
    dataAluguel: date 
    dataDevolucao: date 
    dataEntrega: Optional[date] = None

    #@field_validator('dataAluguel', 'dataDevolucao', 'dataEntrega', pre=True)
    #@classmethod
    #def validate_date_format(cls, v):
    #    if v is not None:
    #        import datetime
    #        try:
    #            datetime.datetime.strptime(v, '%Y-%m-%d')
    #        except ValueError:
    #            raise ValueError(f'Data {v} deve estar no formato YYYY-MM-DD')
    #    return v