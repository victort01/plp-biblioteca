# plp-biblioteca

Sistema de gerenciamento de biblioteca desenvolvido em Python para a disciplina Paradigmas de Linguagens de Programação. Integra orientação a objetos e programação funcional.

## Integrantes

- Arysson André Oliveira da Luz
- Caio Justino de Andrade
- Luiz Henrique Monteiro dos Santos
- Paulo Victor Oliveira de Barros Araújo

## Execução

Requer Python 3.10 ou superior e Git para obter o projeto pelo terminal. Utiliza exclusivamente a biblioteca padrão do Python.

Clone o repositório e entre na pasta criada.

```sh
git clone https://github.com/victort01/plp-biblioteca.git
cd plp-biblioteca
python --version
```

Abra o terminal na pasta do projeto e execute o menu interativo.

```sh
python main.py
```

No Windows, também pode ser utilizado o comando `py -3 main.py`, conforme a instalação do Python.

Em sistemas que disponibilizam o interpretador como `python3`, substitua `python` por `python3` nos comandos. Confira se a versão é 3.10 ou superior. O programa também pode ser executado como pacote, a partir da raiz do repositório.

```sh
python -m plp_biblioteca
```

Para executar uma demonstração independente, com cadastros e datas fixas, use o comando abaixo.

```sh
python main.py --demo
```

A execução equivalente pelo pacote é `python -m plp_biblioteca --demo`. Todos esses comandos devem ser executados na pasta que contém este README. A execução é direta, usando os arquivos do repositório e os módulos incluídos no Python.

O programa trabalha com dados em memória. Cada execução inicia um novo estado. Encerrar o programa descarta os cadastros. O modo demonstrativo cria seus próprios dados e termina ao concluir a apresentação.

## Funcionalidades

- Cadastro e listagem de livros e usuários.
- Identificadores numéricos gerados automaticamente e matrículas únicas.
- Registro de empréstimos com livro, usuário, retirada e data prevista informados.
- Registro de devoluções e liberação do livro para uma nova retirada.
- Consulta dos empréstimos, incluindo os devolvidos.
- Filtragem de livros por categoria.
- Relatório de empréstimos ativos em atraso, multas individuais e total.
- Estatísticas de livros por categoria, empréstimos por usuário, empréstimos ativos, ativos em atraso e valor total das multas.
- Comparação entre filtragem imperativa e funcional.

As datas digitadas no menu seguem o formato `DD/MM/AAAA`. A data prevista é informada em cada retirada. O programa aceita uma devolução prevista no próprio dia da retirada. A multa começa no dia seguinte à data prevista, no valor de R$ 2,00 por dia. A data de referência é sempre informada pelo usuário ao consultar multas e estatísticas.

O relatório considera o estado atual dos empréstimos. Uma devolução registrada exclui o empréstimo do cálculo, inclusive quando a referência informada é anterior à devolução. Essa consulta segue a exigência de considerar apenas empréstimos ativos e atrasados. As contagens de empréstimos por usuário incluem todo o histórico registrado na sessão.

Cada livro representa um exemplar único. O programa impede uma nova retirada enquanto existir um empréstimo ativo daquele livro. Também valida a existência do livro e do usuário, campos obrigatórios, matrículas duplicadas, devoluções repetidas e datas incoerentes. Uma retirada posterior de um livro já devolvido deve ocorrer na mesma data ou depois de todas as devoluções anteriores desse exemplar. Rejeições acontecem antes da alteração das coleções.

Categorias são comparadas desconsiderando maiúsculas e minúsculas. As estatísticas agrupam categorias com essa mesma regra e apresentam seus nomes em minúsculas.

## Organização e orientação a objetos

```text
plp-biblioteca/
├── .gitignore
├── README.md
├── main.py
└── plp_biblioteca/
    ├── __init__.py
    ├── __main__.py
    ├── biblioteca.py
    ├── cli.py
    ├── funcoes.py
    └── modelos.py
```

| Arquivo | Responsabilidade |
| --- | --- |
| `main.py` | Inicia o programa pela raiz do repositório. |
| `plp_biblioteca/__init__.py` | Identifica o pacote Python. |
| `plp_biblioteca/__main__.py` | Permite iniciar o programa com python -m plp_biblioteca. |
| `plp_biblioteca/modelos.py` | Define Livro, Usuario e Emprestimo como dataclasses imutáveis. |
| `plp_biblioteca/biblioteca.py` | Mantém os cadastros e controla os empréstimos e devoluções. |
| `plp_biblioteca/funcoes.py` | Implementa consultas, cálculos, relatório e estatísticas. |
| `plp_biblioteca/cli.py` | Recebe entradas, apresenta resultados e executa a demonstração. |

`Livro` contém identificador, título, autor e categoria. `Usuario` contém identificador, nome e matrícula. `Emprestimo` referencia exatamente um Livro e um Usuario, além de guardar identificador e datas. A propriedade `ativo` indica a ausência de devolução. Um usuário e um livro podem participar de vários empréstimos ao longo do histórico, respeitando o limite de um empréstimo ativo por livro.

`Biblioteca` administra dicionários internos `_livros`, `_usuarios` e `_emprestimos`. O prefixo `_` indica acesso interno por convenção em Python. As propriedades públicas expõem tuplas de objetos imutáveis. Cadastros e devoluções passam pelos métodos da biblioteca, que aplicam as validações.

Na devolução, `dataclasses.replace` cria outra instância de Emprestimo com a data efetiva preenchida. A Biblioteca substitui a entrada em seu dicionário. Uma tupla obtida anteriormente continua contendo a versão anterior do empréstimo, funcionando como um retrato do estado no momento da consulta.

O menu processa uma operação de cada vez, em uma única thread. Uma adaptação com acessos simultâneos exigiria sincronizar a verificação de disponibilidade e o registro do empréstimo na mesma seção crítica. Com persistência, essa garantia também precisaria existir na transação de armazenamento.

## Programação funcional

As funções de `plp_biblioteca/funcoes.py` recebem os dados necessários por parâmetro e preservam suas entradas. As coleções resultantes são novas estruturas. Os valores monetários utilizam Decimal, com a diária fixa criada como `Decimal("2.00")` dentro do relatório.

| Função | Comportamento |
| --- | --- |
| `filtrar_livros` | Usa filter e retorna uma tupla de livros da categoria. |
| `filtrar_livros_imperativo` | Produz o mesmo resultado com for, if e uma lista local. |
| `calcular_dias_atraso` | Calcula a diferença entre referência e previsão, limitada a zero. |
| `calcular_multa` | Multiplica os dias pela diária recebida. Rejeita valores negativos. |
| `selecionar_atrasados` | Usa filter para selecionar empréstimos ativos com previsão anterior à referência. |
| `gerar_relatorio_multas` | Usa a seleção por filter, transforma empréstimos com map e soma multas com reduce. |
| `gerar_estatisticas` | Cria um dicionário com as cinco estatísticas exigidas. Usa reduce nas contagens de empréstimos por usuário e de ativos. |

`gerar_relatorio_multas` devolve um par formado pela tupla de multas individuais e pelo total. Cada multa individual é um par formado pelo empréstimo e pelo valor. O valor inicial `Decimal("0.00")` no reduce garante o total zero quando a coleção estiver vazia.

Por exemplo, `calcular_multa(3, Decimal("2.00"))` devolve `Decimal("6.00")`. A chamada pode ser substituída pelo seu resultado sem alterar o comportamento do cálculo. Nenhuma dessas funções consulta o relógio, imprime resultados ou modifica a biblioteca.

Cadastrar e devolver alteram o estado da Biblioteca. Ler o teclado e imprimir no terminal também produzem efeitos observáveis. Essas operações ficam nos métodos de gerenciamento e na interface, enquanto o cálculo permanece em funções puras.

## Comparação entre paradigmas

A opção 11 executa `filtrar_livros` e `filtrar_livros_imperativo` com a mesma coleção e categoria. Exibe os dois resultados e compara a igualdade das tuplas, incluindo a ordem dos livros.

A versão imperativa descreve o percurso e acumula os encontrados em uma lista local. A funcional expressa a seleção por um predicado passado ao filter. Ambas preservam a coleção original e devolvem tuplas. A mutação da lista local na versão imperativa permanece interna à função e permite que ela também tenha comportamento puro.

## Roteiro de demonstração

Execute `python main.py --demo` para verificar o cenário abaixo, com referência em 10/11/2026.

| Livro | Previsão | Situação | Multa |
| --- | --- | --- | --- |
| Dom Casmurro | 07/11/2026 | Ativo, com três dias de atraso | R$ 6,00 |
| O Cortiço | 10/11/2026 | Ativo, com vencimento na referência | R$ 0,00 |
| Python para Todos | 05/11/2026 | Devolvido em 08/11/2026 | Excluído do relatório |
| A Metamorfose | 09/11/2026 | Ativo, com um dia de atraso | R$ 2,00 |

O primeiro relatório totaliza R$ 8,00. As estatísticas mostram três empréstimos ativos, dois ativos em atraso e dois empréstimos por usuário. A comparação de paradigmas retorna resultados equivalentes e a conferência das consultas mostra que os empréstimos foram preservados.

A demonstração tenta uma segunda retirada de Dom Casmurro e mostra a recusa. Em seguida, registra sua devolução e emite outro relatório, agora com total de R$ 2,00. Por fim, registra uma nova retirada do mesmo livro.

Para exercitar o menu manualmente, cadastre primeiro os livros e usuários, utilize os identificadores exibidos na retirada e consulte o relatório com uma referência posterior ao vencimento. Após a devolução, consulte novamente para observar a exclusão da multa e a disponibilidade do exemplar.
