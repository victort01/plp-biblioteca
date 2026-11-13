from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Livro:
    identificador: int
    titulo: str
    autor: str
    categoria: str


@dataclass(frozen=True)
class Usuario:
    identificador: int
    nome: str
    matricula: str


@dataclass(frozen=True)
class Emprestimo:
    identificador: int
    livro: Livro
    usuario: Usuario
    data_emprestimo: date
    data_prevista: date
    data_devolucao: date | None = None

    @property
    def ativo(self) -> bool:
        return self.data_devolucao is None
