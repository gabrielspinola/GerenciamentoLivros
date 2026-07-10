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
    dataAluguel_raw: str = ""
    dataDevolucao_raw: str = ""
    dataEntrega_raw: str = ""

    def to_dict(self) -> dict:
        # Converte para dicionário
        data = asdict(self)
        if self.dataAluguel:
            data['dataAluguel'] = self.dataAluguel.isoformat()
        if self.dataDevolucao:
            data['dataDevolucao'] = self.dataDevolucao.isoformat()
        if self.dataEntrega:
            data['dataEntrega'] = self.dataEntrega.isoformat()
        return data        

    @classmethod
    def from_row(cls, row: tuple) -> 'LivrosAlugadosModel':
        # Cria instância a partir de uma linha do banco
        return cls(
            idLivrosAlugados=row[0],
            idusuario=row[1],
            nome=row[2],
            idlivro=row[3],
            titulo=row[4],
            dataAluguel_raw=row[5].strftime("%d/%m/%Y") if row[5] else '',
            dataDevolucao_raw=row[6].strftime("%d/%m/%Y") if row[6] else '',
            dataEntrega_raw=row[7].strftime("%d/%m/%Y") if row[7] else "",
            dataAluguel=row[5],
            dataDevolucao=row[6],
            dataEntrega=row[7],
        )