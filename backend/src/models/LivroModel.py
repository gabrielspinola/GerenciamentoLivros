from dataclasses import dataclass, asdict, field
from typing import Dict, Any


@dataclass
class LivroModel:
    idlivro: int
    titulo: str
    autor: str
    ano_publicacao: int
    genero: str
    bloqueado: str = "N"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LivroModel':
        return cls(
            idlivro=data.get("idlivro", 0),
            titulo=data["titulo"],
            autor=data["autor"],
            ano_publicacao=int(data["ano_publicacao"]),
            genero=data["genero"],
            bloqueado=data.get("bloqueado", "N")
        )

    @classmethod
    def from_row(cls, row: tuple) -> 'LivroModel':
        # Cria instância a partir de uma linha do banco
        return cls(
            idlivro=row[0],
            titulo=row[1],
            autor=row[2],
            ano_publicacao=row[3],
            genero=row[4],
            bloqueado=row[5]
        )
