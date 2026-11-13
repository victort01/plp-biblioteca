import argparse
from datetime import date, datetime
from decimal import Decimal

from .biblioteca import Biblioteca
from .funcoes import (
    calcular_dias_atraso,
    filtrar_livros,
    filtrar_livros_imperativo,
    gerar_estatisticas,
    gerar_relatorio_multas,
)


def ler_data(mensagem: str) -> date:
    return datetime.strptime(input(mensagem).strip(), "%d/%m/%Y").date()


def formatar_dinheiro(valor: Decimal) -> str:
    return f"R$ {valor:.2f}".replace(".", ",")


def exibir_livros(livros):
    if not livros:
        print("Nenhum livro encontrado.")
    for livro in livros:
        print(f"{livro.identificador} | {livro.titulo} | {livro.autor} | {livro.categoria}")


def exibir_usuarios(usuarios):
    if not usuarios:
        print("Nenhum usuário encontrado.")
    for usuario in usuarios:
        print(f"{usuario.identificador} | {usuario.nome} | matrícula {usuario.matricula}")


def exibir_emprestimos(emprestimos):
    if not emprestimos:
        print("Nenhum empréstimo encontrado.")
    for emprestimo in emprestimos:
        situacao = "Ativo"
        if emprestimo.data_devolucao is not None:
            situacao = f"Devolvido em {emprestimo.data_devolucao:%d/%m/%Y}"
        print(
            f"{emprestimo.identificador} | {emprestimo.livro.titulo} | {emprestimo.usuario.nome}"
            f" | retirada {emprestimo.data_emprestimo:%d/%m/%Y}"
            f" | prevista {emprestimo.data_prevista:%d/%m/%Y} | {situacao}"
        )


def exibir_relatorio(emprestimos, referencia):
    multas, total = gerar_relatorio_multas(emprestimos, referencia)
    print(f"Multas em {referencia:%d/%m/%Y}")
    if not multas:
        print("Nenhum empréstimo ativo em atraso.")
    for emprestimo, multa in multas:
        dias = calcular_dias_atraso(emprestimo.data_prevista, referencia)
        print(
            f"Empréstimo {emprestimo.identificador} | {emprestimo.livro.titulo}"
            f" | {emprestimo.usuario.nome} | {dias} dia(s) | {formatar_dinheiro(multa)}"
        )
    print(f"Total: {formatar_dinheiro(total)}")


def exibir_estatisticas(biblioteca, referencia):
    dados = gerar_estatisticas(
        biblioteca.livros, biblioteca.usuarios, biblioteca.emprestimos, referencia,
    )
    print(f"Estatísticas em {referencia:%d/%m/%Y}")
    print("Livros por categoria:")
    for categoria, quantidade in dados["livros_por_categoria"].items():
        print(f"  {categoria}: {quantidade}")
    print("Empréstimos por usuário (inclui devolvidos):")
    for usuario in biblioteca.usuarios:
        print(f"  {usuario.nome}: {dados['emprestimos_por_usuario'][usuario.identificador]}")
    print(f"Empréstimos ativos: {dados['emprestimos_ativos']}")
    print(f"Empréstimos ativos em atraso: {dados['emprestimos_ativos_atrasados']}")
    print(f"Total das multas: {formatar_dinheiro(dados['total_multas'])}")


def comparar_paradigmas(livros, categoria):
    funcional = filtrar_livros(livros, categoria)
    imperativo = filtrar_livros_imperativo(livros, categoria)
    print("Resultado funcional:")
    exibir_livros(funcional)
    print("Resultado imperativo:")
    exibir_livros(imperativo)
    print(f"Resultados equivalentes: {funcional == imperativo}")


def executar_demonstracao():
    biblioteca = Biblioteca()
    biblioteca.cadastrar_livro("Dom Casmurro", "Machado de Assis", "Literatura")
    biblioteca.cadastrar_livro("O Cortiço", "Aluísio Azevedo", "Literatura")
    biblioteca.cadastrar_livro("Python para Todos", "Charles Severance", "Programação")
    biblioteca.cadastrar_livro("A Metamorfose", "Franz Kafka", "Literatura")
    biblioteca.cadastrar_usuario("Leitor A", "DEMO001")
    biblioteca.cadastrar_usuario("Leitor B", "DEMO002")
    biblioteca.registrar_emprestimo(1, 1, date(2026, 11, 1), date(2026, 11, 7))
    biblioteca.registrar_emprestimo(2, 1, date(2026, 11, 2), date(2026, 11, 10))
    biblioteca.registrar_emprestimo(3, 2, date(2026, 11, 1), date(2026, 11, 5))
    biblioteca.registrar_emprestimo(4, 2, date(2026, 11, 2), date(2026, 11, 9))
    biblioteca.registrar_devolucao(3, date(2026, 11, 8))
    referencia = date(2026, 11, 10)
    print("DEMONSTRAÇÃO COM DADOS FIXOS")
    exibir_emprestimos(biblioteca.emprestimos)
    antes = biblioteca.emprestimos
    exibir_relatorio(antes, referencia)
    exibir_estatisticas(biblioteca, referencia)
    comparar_paradigmas(biblioteca.livros, "Literatura")
    print(f"Consultas preservaram os empréstimos: {antes == biblioteca.emprestimos}")
    try:
        biblioteca.registrar_emprestimo(1, 2, referencia, date(2026, 11, 17))
    except ValueError as erro:
        print(f"Segunda retirada recusada: {erro}")
    biblioteca.registrar_devolucao(1, referencia)
    print("Após devolver Dom Casmurro:")
    exibir_relatorio(biblioteca.emprestimos, referencia)
    biblioteca.registrar_emprestimo(1, 2, referencia, date(2026, 11, 17))
    print("Nova retirada de Dom Casmurro registrada após a devolução.")


def executar_menu():
    biblioteca = Biblioteca()
    while True:
        print(
            "\nPLP Biblioteca\n"
            "1 - Cadastrar livro\n2 - Cadastrar usuário\n"
            "3 - Listar livros\n4 - Listar usuários\n"
            "5 - Registrar empréstimo\n6 - Registrar devolução\n"
            "7 - Consultar empréstimos\n8 - Filtrar livros por categoria\n"
            "9 - Relatório de multas e atrasos\n10 - Estatísticas\n"
            "11 - Comparar paradigmas\n0 - Sair"
        )
        try:
            opcao = input("Opção: ").strip()
            match opcao:
                case "0":
                    return
                case "1":
                    livro = biblioteca.cadastrar_livro(
                        input("Título: "), input("Autor: "), input("Categoria: "),
                    )
                    print(f"Livro cadastrado com identificador {livro.identificador}.")
                case "2":
                    usuario = biblioteca.cadastrar_usuario(input("Nome: "), input("Matrícula: "))
                    print(f"Usuário cadastrado com identificador {usuario.identificador}.")
                case "3":
                    exibir_livros(biblioteca.livros)
                case "4":
                    exibir_usuarios(biblioteca.usuarios)
                case "5":
                    emprestimo = biblioteca.registrar_emprestimo(
                        int(input("Identificador do livro: ")),
                        int(input("Identificador do usuário: ")),
                        ler_data("Data da retirada (DD/MM/AAAA): "),
                        ler_data("Data prevista (DD/MM/AAAA): "),
                    )
                    print(f"Empréstimo registrado com identificador {emprestimo.identificador}.")
                case "6":
                    biblioteca.registrar_devolucao(
                        int(input("Identificador do empréstimo: ")),
                        ler_data("Data da devolução (DD/MM/AAAA): "),
                    )
                    print("Devolução registrada. Livro disponível.")
                case "7":
                    exibir_emprestimos(biblioteca.emprestimos)
                case "8":
                    exibir_livros(filtrar_livros(biblioteca.livros, input("Categoria: ")))
                case "9":
                    exibir_relatorio(biblioteca.emprestimos, ler_data("Referência (DD/MM/AAAA): "))
                case "10":
                    exibir_estatisticas(biblioteca, ler_data("Referência (DD/MM/AAAA): "))
                case "11":
                    comparar_paradigmas(biblioteca.livros, input("Categoria: "))
                case _:
                    print("Opção inválida.")
        except ValueError as erro:
            print(f"Entrada recusada: {erro}")


def main():
    parser = argparse.ArgumentParser(description="Sistema de gerenciamento de biblioteca.")
    parser.add_argument("--demo", action="store_true", help="Executar demonstração com dados fixos.")
    argumentos = parser.parse_args()
    try:
        if argumentos.demo:
            executar_demonstracao()
        else:
            executar_menu()
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma encerrado.")


if __name__ == "__main__":
    main()
