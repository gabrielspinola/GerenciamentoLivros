from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class SettingsModel:
    idsettings: Optional[int] = None
    diasLivroEmprestado: int = 0
    createdAt: str = ""
    updatedAt: str = ""
    
    def to_dict(self) -> dict:
        # Converte para dicionário
        return asdict(self)
    
    @classmethod
    def from_row(cls, row: tuple) -> 'SettingsModel':
        # Cria instância a partir de uma linha do banco
        return cls(
            idsettings=row[0],
            diasLivroEmprestado=row[1],
            createdAt=row[2],
            updatedAt=row[3]
        )