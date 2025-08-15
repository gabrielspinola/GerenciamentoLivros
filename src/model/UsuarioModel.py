from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

@dataclass
class UsuarioModel:
    idusuario: Optional[int] = None
    nome: str = ""
    login: str = ""
    password: str = ""
    dataAniversario: datetime = None

    def to_dict(self) -> dict:
        """Converte para dicionário"""
        data = asdict(self)
        if self.dataAniversario:
            data['dataAniversario'] = self.dataAniversario.isoformat()
        return data
    
    @classmethod
    def from_row(cls, row: tuple) -> 'UsuarioModel':
        """Cria instância a partir de uma linha do banco"""
        return cls(
            idusuario=row[0],
            nome=row[1],
            login=row[2],
            password=row[3],
            dataAniversario=row[4]
        )
