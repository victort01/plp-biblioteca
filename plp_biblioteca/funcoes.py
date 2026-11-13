from collections.abc import Sequence
from datetime import date
from decimal import Decimal
from functools import reduce

from .modelos import Emprestimo, Livro, Usuario


def filtrar_livros(livros: Sequence[Livro], categoria: str) -> tuple[Livro, ...]:
    return tuple(filter(lambda livro: livro.categoria.casefold() == categoria.strip().casefold(), livros))


def filtrar_livros_imperativo(livros: Sequence[Livro], categoria: str) -> tuple[Livro, ...]:
    encontrados = []
    for livro in livros:
        if livro.categoria.casefold() == categoria.strip().casefold():
            encontrados.append(livro)
    return tuple(encontrados)


def calcular_dias_atraso(data_prevista: date, referencia: date) -> int:
    return max(0, (referencia - data_prevista).days)


def calcular_multa(dias_atraso: int, diaria: Decimal) -> Decimal:
    if dias_atraso < 0 or diaria < 0:
        raise ValueError("Dias de atraso e multa diária devem ser não negativos.")
    return dias_atraso * diaria


def selecionar_atrasados(
    emprestimos: Sequence[Emprestimo], referencia: date,
) -> tuple[Emprestimo, ...]:
    return tuple(filter(lambda e: e.ativo and e.data_prevista < referencia, emprestimos))


def gerar_relatorio_multas(
    emprestimos: Sequence[Emprestimo], referencia: date,
) -> tuple[tuple[tuple[Emprestimo, Decimal], ...], Decimal]:
    atrasados = selecionar_atrasados(emprestimos, referencia)
    multas = tuple(map(
        lambda e: (e, calcular_multa(calcular_dias_atraso(e.data_prevista, referencia), Decimal("2.00"))),
        atrasados,
    ))
    total = reduce(lambda acumulado, item: acumulado + item[1], multas, Decimal("0.00"))
    return multas, total


def gerar_estatisticas(
    livros: Sequence[Livro], usuarios: Sequence[Usuario],
    emprestimos: Sequence[Emprestimo], referencia: date,
) -> dict:
    categorias = tuple(dict.fromkeys(map(lambda livro: livro.categoria.casefold(), livros)))
    por_categoria = {
        categoria: len(filtrar_livros(livros, categoria)) for categoria in categorias
    }
    por_usuario = {
        usuario.identificador: reduce(
            lambda total, e: total + int(e.usuario.identificador == usuario.identificador),
            emprestimos, 0,
        )
        for usuario in usuarios
    }
    ativos = reduce(lambda total, e: total + int(e.ativo), emprestimos, 0)
    atrasados = selecionar_atrasados(emprestimos, referencia)
    _, multas = gerar_relatorio_multas(emprestimos, referencia)
    return {
        "livros_por_categoria": por_categoria,
        "emprestimos_por_usuario": por_usuario,
        "emprestimos_ativos": ativos,
        "emprestimos_ativos_atrasados": len(atrasados),
        "total_multas": multas,
    }
