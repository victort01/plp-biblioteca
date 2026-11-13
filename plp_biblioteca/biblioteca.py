from dataclasses import replace
from datetime import date

from .modelos import Emprestimo, Livro, Usuario


class Biblioteca:
    def __init__(self):
        self._livros: dict[int, Livro] = {}
        self._usuarios: dict[int, Usuario] = {}
        self._emprestimos: dict[int, Emprestimo] = {}

    @property
    def livros(self) -> tuple[Livro, ...]:
        return tuple(self._livros.values())

    @property
    def usuarios(self) -> tuple[Usuario, ...]:
        return tuple(self._usuarios.values())

    @property
    def emprestimos(self) -> tuple[Emprestimo, ...]:
        return tuple(self._emprestimos.values())

    def cadastrar_livro(self, titulo: str, autor: str, categoria: str) -> Livro:
        if not all(campo.strip() for campo in (titulo, autor, categoria)):
            raise ValueError("Título, autor e categoria são obrigatórios.")
        identificador = len(self._livros) + 1
        livro = Livro(identificador, titulo.strip(), autor.strip(), categoria.strip())
        self._livros[identificador] = livro
        return livro

    def cadastrar_usuario(self, nome: str, matricula: str) -> Usuario:
        if not nome.strip() or not matricula.strip():
            raise ValueError("Nome e matrícula são obrigatórios.")
        if any(u.matricula == matricula.strip() for u in self.usuarios):
            raise ValueError("Matrícula já cadastrada.")
        identificador = len(self._usuarios) + 1
        usuario = Usuario(identificador, nome.strip(), matricula.strip())
        self._usuarios[identificador] = usuario
        return usuario

    def consultar_livro(self, identificador: int) -> Livro:
        if identificador not in self._livros:
            raise ValueError("Livro não encontrado.")
        return self._livros[identificador]

    def consultar_usuario(self, identificador: int) -> Usuario:
        if identificador not in self._usuarios:
            raise ValueError("Usuário não encontrado.")
        return self._usuarios[identificador]

    def consultar_emprestimo(self, identificador: int) -> Emprestimo:
        if identificador not in self._emprestimos:
            raise ValueError("Empréstimo não encontrado.")
        return self._emprestimos[identificador]

    def registrar_emprestimo(
        self, livro_id: int, usuario_id: int,
        data_emprestimo: date, data_prevista: date,
    ) -> Emprestimo:
        livro = self.consultar_livro(livro_id)
        usuario = self.consultar_usuario(usuario_id)
        if data_prevista < data_emprestimo:
            raise ValueError("A data prevista deve ser igual ou posterior à retirada.")
        anteriores = tuple(e for e in self.emprestimos if e.livro == livro)
        if any(e.ativo for e in anteriores):
            raise ValueError("Livro já emprestado.")
        if any(e.data_devolucao > data_emprestimo for e in anteriores):
            raise ValueError("A retirada deve ser igual ou posterior às devoluções anteriores.")
        identificador = len(self._emprestimos) + 1
        emprestimo = Emprestimo(
            identificador, livro, usuario, data_emprestimo, data_prevista,
        )
        self._emprestimos[identificador] = emprestimo
        return emprestimo

    def registrar_devolucao(self, emprestimo_id: int, data_devolucao: date) -> Emprestimo:
        emprestimo = self.consultar_emprestimo(emprestimo_id)
        if not emprestimo.ativo:
            raise ValueError("Empréstimo já devolvido.")
        if data_devolucao < emprestimo.data_emprestimo:
            raise ValueError("A devolução deve ser igual ou posterior à retirada.")
        atualizado = replace(emprestimo, data_devolucao=data_devolucao)
        self._emprestimos[emprestimo_id] = atualizado
        return atualizado
