"""Utilitários compartilhados da trilha T2 (aluno e corretor). Não precisa editar."""
import copy
import importlib.util
import json
import math
import sys
from pathlib import Path

FUNCOES_POR_FASE = {
    1: ["total_item", "total_pedido", "esta_pago"],
    2: ["aplicar_status", "adicionar_item", "cancelar"],
    3: ["pedidos_pagos", "faturamento", "totais_por_eixo", "top_n"],
    4: ["criar_regra_desconto", "aplicar_desconto", "aplicar_frete", "compor", "preco_final"],
    5: ["gerar_relatorio"],
}
PESOS = {1: 10, 2: 15, 3: 25, 4: 25, 5: 20}
NOMES_FASES = {
    1: "Funções puras",
    2: "Imutabilidade",
    3: "map, filter e reduce",
    4: "Ordem superior, closures e composição",
    5: "Pipeline integrado",
}


def fase_da_funcao(nome):
    for fase, funcoes in FUNCOES_POR_FASE.items():
        if nome in funcoes:
            return fase
    return None


def carregar_modulo(caminho, nome="funcional_aluno"):
    caminho = Path(caminho)
    spec = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nome] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def normalizar(obj):
    """Converte para tipos JSON (tuplas viram listas, conjuntos viram listas ordenadas)."""
    def padrao(o):
        if isinstance(o, (set, frozenset)):
            return sorted(o)
        return str(o)
    return json.loads(json.dumps(obj, default=padrao))


def iguais(a, b, tol=0.011):
    """Comparação tolerante a centavos, para números, listas e dicionários."""
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= tol
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(iguais(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(iguais(a[k], b[k], tol) for k in a)
    return a == b


def chamar(funcao, args):
    """Chama a função duas vezes com cópias dos argumentos.

    Detecta: erro, mutação dos argumentos (imutabilidade) e resultados diferentes
    para a mesma entrada (pureza).
    """
    original = copy.deepcopy(args)
    a1 = copy.deepcopy(args)
    a2 = copy.deepcopy(args)
    try:
        r1 = funcao(*a1)
        r2 = funcao(*a2)
    except Exception as erro:  # noqa: BLE001 - queremos capturar qualquer erro do aluno
        return {"erro": f"{type(erro).__name__}: {erro}".rstrip(": ")}
    n1, n2 = normalizar(r1), normalizar(r2)
    return {
        "r1": n1,
        "r2": n2,
        "mutou": (a1 != original) or (a2 != original),
        "impura": n1 != n2,
    }


# Funções auxiliares usadas em testes de compor (iguais no aluno e no corretor)
FUNCOES_TESTE = {
    "inc": lambda x: x + 1,
    "dobro": lambda x: x * 2,
    "quadrado": lambda x: x * x,
}


def executar_caso(modulo, caso):
    """Executa um caso de teste (formato comum ao conferir.py e ao corretor)."""
    tipo = caso.get("kind", "call")
    try:
        if tipo == "call":
            funcao = getattr(modulo, caso["funcao"])
            return chamar(funcao, caso["args"])
        if tipo == "regra":
            def envelope(politica, pedidos, categoria):
                regra = modulo.criar_regra_desconto(politica, pedidos, categoria)
                return [regra(p) for p in pedidos]
            return chamar(envelope, caso["args"])
        if tipo == "compor":
            def envelope(nome_f, nome_g, x):
                return modulo.compor(FUNCOES_TESTE[nome_f], FUNCOES_TESTE[nome_g])(x)
            return chamar(envelope, caso["args"])
        if tipo == "preco_final":
            def envelope(pedido, taxa):
                return modulo.preco_final(pedido, lambda p: taxa)
            return chamar(envelope, caso["args"])
        if tipo == "aplicar_desconto":
            def envelope(pedido, taxa):
                return modulo.aplicar_desconto(pedido, lambda p: taxa)
            return chamar(envelope, caso["args"])
        return {"erro": f"tipo de caso desconhecido: {tipo}"}
    except AttributeError:
        return {"erro": "função não definida em funcional.py"}
    except Exception as erro:  # noqa: BLE001
        return {"erro": f"{type(erro).__name__}: {erro}"}
