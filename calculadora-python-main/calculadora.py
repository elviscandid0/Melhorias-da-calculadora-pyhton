#!/usr/bin/env python3
"""
Calculadora em Python — Operações Básicas, Porcentagem e Histórico Completo de Cálculos
Suporta soma, subtração, multiplicação, divisão, porcentagem, expressões encadeadas
e registro contínuo de todo o histórico de operações.
"""

import ast
from datetime import datetime
from typing import Callable, Dict, List, TypedDict


class RegistroCalculo(TypedDict):
    indice: int
    horario: str
    expressao: str
    chamada_python: str
    resultado: str
    sucesso: bool


# Lista em memória que mantém todo o histórico de cálculos da sessão
HISTORICO_CALCULOS: List[RegistroCalculo] = []


def somar(a: float, b: float) -> float:
    """Retorna a soma entre dois números (a + b)."""
    return a + b


def subtrair(a: float, b: float) -> float:
    """Retorna a diferença entre dois números (a - b)."""
    return a - b


def multiplicar(a: float, b: float) -> float:
    """Retorna o produto entre dois números (a * b)."""
    return a * b


def dividir(a: float, b: float) -> float:
    """Retorna o quociente entre dois números (a / b).

    Levanta ZeroDivisionError caso o divisor seja zero.
    """
    if b == 0:
        raise ZeroDivisionError("Não é possível dividir um número por zero.")
    return a / b


def porcentagem(a: float, b: float) -> float:
    """Retorna 'b' por cento de 'a' ((a * b) / 100)."""
    return (a * b) / 100


OPERACOES: Dict[str, Callable[[float, float], float]] = {
    "+": somar,
    "-": subtrair,
    "*": multiplicar,
    "/": dividir,
    "%": porcentagem,
}

NOMES_FUNCOES: Dict[str, str] = {
    "+": "somar",
    "-": "subtrair",
    "*": "multiplicar",
    "/": "dividir",
    "%": "porcentagem",
}


def formatar_numero(valor: float) -> str:
    """Formata um número removendo casas decimais desnecessárias (.0)."""
    if valor == 0:
        return "0"
    if isinstance(valor, int):
        return str(valor)
    if valor.is_integer() and abs(valor) < 1e15:
        return str(int(valor))
    return f"{valor:.10g}"


def registrar_no_historico(
    expressao: str, chamada_python: str, resultado: str, sucesso: bool = True
) -> RegistroCalculo:
    """Adiciona uma operação ao histórico acumulado sem sobrescrever anteriores."""
    item: RegistroCalculo = {
        "indice": len(HISTORICO_CALCULOS) + 1,
        "horario": datetime.now().strftime("%H:%M:%S"),
        "expressao": expressao,
        "chamada_python": chamada_python,
        "resultado": resultado,
        "sucesso": sucesso,
    }
    HISTORICO_CALCULOS.append(item)
    return item


def obter_historico() -> List[RegistroCalculo]:
    """Retorna a lista completa de todos os cálculos realizados."""
    return list(HISTORICO_CALCULOS)


def limpar_historico() -> None:
    """Limpa todos os registros do histórico de cálculos."""
    HISTORICO_CALCULOS.clear()


def calcular(a: float, operacao: str, b: float) -> float:
    """Executa a operação entre 'a' e 'b' e armazena no histórico completo."""
    if operacao not in OPERACOES:
        raise ValueError(f"Operação inválida: '{operacao}'. Use +, -, *, / ou %.")

    nome_funcao = NOMES_FUNCOES[operacao]
    expressao = f"{formatar_numero(a)} {operacao} {formatar_numero(b)}"
    chamada = f"{nome_funcao}({formatar_numero(a)}, {formatar_numero(b)})"

    try:
        resultado = OPERACOES[operacao](a, b)
        registrar_no_historico(expressao, chamada, formatar_numero(resultado), True)
        return resultado
    except ZeroDivisionError as erro:
        registrar_no_historico(expressao, chamada, f"ZeroDivisionError: {erro}", False)
        raise


def calcular_expressao(expressao: str) -> Dict[str, object]:
    """Avalia uma expressão aritmética completa (ex: '10 + 5 * 2 - 4') com segurança,
    registrando cada etapa intermediária e o cálculo completo.
    """
    arvore = ast.parse(expressao.replace(",", "."), mode="eval")
    passos: List[Dict[str, object]] = []

    mapa_ast = {
        ast.Add: "+",
        ast.Sub: "-",
        ast.Mult: "*",
        ast.Div: "/",
        ast.Mod: "%",
    }

    def avaliar_no(no: ast.AST) -> tuple[float, str]:
        if isinstance(no, ast.Expression):
            return avaliar_no(no.body)
        if isinstance(no, ast.Constant) and isinstance(no.value, (int, float)):
            val = float(no.value)
            return val, formatar_numero(val)
        if isinstance(no, ast.UnaryOp) and isinstance(no.op, (ast.UAdd, ast.USub)):
            val, repr_filho = avaliar_no(no.operand)
            if isinstance(no.op, ast.USub):
                return -val, f"-{repr_filho}"
            return val, repr_filho
        if isinstance(no, ast.BinOp) and type(no.op) in mapa_ast:
            esq_val, esq_repr = avaliar_no(no.left)
            dir_val, dir_repr = avaliar_no(no.right)
            simbolo = mapa_ast[type(no.op)]
            nome_fn = NOMES_FUNCOES[simbolo]
            res = calcular(esq_val, simbolo, dir_val)
            chamada_aninhada = f"{nome_fn}({esq_repr}, {dir_repr})"
            passos.append(
                {
                    "a": esq_val,
                    "operacao": simbolo,
                    "b": dir_val,
                    "funcao": nome_fn,
                    "chamada": f"{nome_fn}({formatar_numero(esq_val)}, {formatar_numero(dir_val)})",
                    "resultado": res,
                    "resultadoFormatado": formatar_numero(res),
                }
            )
            return res, chamada_aninhada
        raise ValueError("Expressão contém operadores não suportados. Use +, -, *, /, % e parênteses.")

    valor_final, chamada_completa = avaliar_no(arvore)
    return {
        "resultado": valor_final,
        "resultadoFormatado": formatar_numero(valor_final),
        "chamadaCompleta": chamada_completa,
        "passos": passos,
    }


def exibir_historico_terminal() -> None:
    """Imprime no terminal todo o histórico acumulado de cálculos."""
    if not HISTORICO_CALCULOS:
        print("\nNenhum cálculo registrado até o momento.")
        return

    print("\n" + "-" * 54)
    print(" HISTÓRICO COMPLETO DE CÁLCULOS")
    print("-" * 54)
    for item in HISTORICO_CALCULOS:
        print(
            f" #{item['indice']:02d} [{item['horario']}] "
            f"{item['expressao']} = {item['resultado']}  ({item['chamada_python']})"
        )
    print("-" * 54)


def menu_interativo() -> None:
    """Executa a calculadora de forma interativa mantendo todo o histórico."""
    opcoes_menu = {
        "1": ("+", "Soma"),
        "2": ("-", "Subtração"),
        "3": ("*", "Multiplicação"),
        "4": ("/", "Divisão"),
        "5": ("%", "Porcentagem"),
    }

    acumulador: float | None = None
    trilha_expressao = ""

    print("=" * 54)
    print("   CALCULADORA EM PYTHON COM HISTÓRICO CONTÍNUO")
    print("=" * 54)

    while True:
        if acumulador is not None:
            print(f"\nCálculo atual acumulado: {trilha_expressao} = {formatar_numero(acumulador)}")

        print("\nEscolha uma opção:")
        print("  [1] Soma (+)")
        print("  [2] Subtração (-)")
        print("  [3] Multiplicação (*)")
        print("  [4] Divisão (/)")
        print("  [5] Porcentagem (%)")
        print("  [6] Avaliar expressão completa (ex: 10 + 5 * 2 - 4 ou 200 % 15)")
        print("  [7] Ver histórico completo de cálculos")
        print("  [8] Reiniciar acumulador atual")
        print("  [0] Sair")

        escolha = input("\nDigite sua opção: ").strip()

        if escolha == "0":
            exibir_historico_terminal()
            print("Encerrando a calculadora. Até logo!")
            break

        if escolha == "7":
            exibir_historico_terminal()
            continue

        if escolha == "8":
            acumulador = None
            trilha_expressao = ""
            print("Acumulador reiniciado. O histórico geral permanece salvo.")
            continue

        if escolha == "6":
            expr = input("Digite a expressão completa: ").strip()
            try:
                dados = calcular_expressao(expr)
                acumulador = float(dados["resultado"])
                trilha_expressao = f"({expr})"
                print(f"\nResultado: {expr} = {dados['resultadoFormatado']}")
                print(f" Composição Python: {dados['chamadaCompleta']}")
            except Exception as erro:
                print(f"Erro ao avaliar expressão: {erro}")
            continue

        if escolha not in opcoes_menu:
            print("Opção inválida. Escolha um número entre 0 e 8.")
            continue

        simbolo, nome = opcoes_menu[escolha]

        try:
            if acumulador is not None:
                usar_anterior = (
                    input(f"Usar resultado anterior ({formatar_numero(acumulador)}) como 1º número? [S/n]: ")
                    .strip()
                    .lower()
                )
                if usar_anterior in ("", "s", "sim"):
                    a = acumulador
                else:
                    a = float(input("Digite o primeiro número: ").strip().replace(",", "."))
                    trilha_expressao = ""
            else:
                a = float(input("Digite o primeiro número: ").strip().replace(",", "."))

            if simbolo == "%":
                b = float(
                    input(f"Digite a taxa de porcentagem a calcular de {formatar_numero(a)} (%): ")
                    .strip()
                    .replace(",", ".")
                )
            else:
                b = float(input("Digite o segundo número: ").strip().replace(",", "."))

            resultado = calcular(a, simbolo, b)

            if trilha_expressao:
                trilha_expressao = f"({trilha_expressao} {simbolo} {formatar_numero(b)})"
            else:
                trilha_expressao = f"{formatar_numero(a)} {simbolo} {formatar_numero(b)}"

            acumulador = resultado
            if simbolo == "%":
                print(f"\nPasso ({nome}): {formatar_numero(b)}% de {formatar_numero(a)} = {formatar_numero(resultado)}")
            else:
                print(f"\nPasso ({nome}): {formatar_numero(a)} {simbolo} {formatar_numero(b)} = {formatar_numero(resultado)}")
            print(f"Cálculo completo até agora: {trilha_expressao} = {formatar_numero(acumulador)}")
        except ValueError:
            print("Erro: Digite apenas valores numéricos válidos.")
        except ZeroDivisionError as erro:
            print(f"Erro matemático: {erro}")


if __name__ == "__main__":
    menu_interativo()
