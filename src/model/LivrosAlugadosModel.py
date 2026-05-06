from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class LivrosAlugadosModel:
    idLivrosAlugados: Optional[int] = None
    idusuario: int = 0
    nome: str = ""
    idlivro: int = 0
    titulo: str = ""
    dataAluguel: str = ""
    dataDevolucao: str = ""
    dataEntrega: str = ""

    def to_dict(self) -> dict:
        # Converte para dicionário
        return asdict(self)

    @classmethod
    def from_row(cls, row: tuple) -> 'LivrosAlugadosModel':
        # Cria instância a partir de uma linha do banco
        return cls(
            idLivrosAlugados=row[0],
            idusuario=row[1],
            nome=row[2],
            idlivro=row[3],
            titulo=row[4],
            dataAluguel=row[5].strftime("%d/%m/%Y") if row[5] else '',
            dataDevolucao=row[6].strftime("%d/%m/%Y") if row[6] else '',
            dataEntrega=row[7].strftime("%d/%m/%Y") if row[7] else "",
        )