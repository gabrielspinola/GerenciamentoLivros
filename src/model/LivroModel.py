from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class LivroModel:
    idlivro: Optional[int] = None
    titulo: str = ""
    autor: str = ""
    ano_publicacao: int = 0
    genero: str = ""

    def to_dict(self) -> dict:
        # Converte para dicionário
        return asdict(self)

    @classmethod
    def from_row(cls, row: tuple) -> 'LivroModel':
        # Cria instância a partir de uma linha do banco
        return cls(
            idlivro=row[0],
            titulo=row[1],
            autor=row[2],
            ano_publicacao=row[3],
            genero=row[4]
        )
