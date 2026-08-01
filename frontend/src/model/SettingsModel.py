from pydantic import BaseModel, model_validator
from typing import Optional

class SettingsModel(BaseModel):
    idsettings: Optional[int] = None
    diasLivroEmprestado: int = 0
    
    @model_validator(mode="after")
    def Valida(self) -> "SettingsModel":
        return self
 
class SettingsModelVazio():
    idsettings: int
    diasLivroEmprestado: int