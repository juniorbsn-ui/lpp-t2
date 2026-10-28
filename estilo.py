"""Verificador de estilo funcional (análise estática do funcional.py).

Regras para as funções do núcleo (tudo menos main):
  - sem global/nonlocal;
  - sem laços for/while (use comprehensions, map, filter, reduce, sum...);
  - sem atribuição aumentada (+=, -=...), que indica acumulador;
  - sem alterar objetos no lugar (x[k] = v, x.atributo = v, del);
  - sem chamar métodos que alteram (append, sort, update...);
  - sem print/input/open nem dependências externas (relógio, aleatório);
  - preco_final deve usar compor.
"""
import ast

from util_t2 import FUNCOES_POR_FASE

PROIBIDAS = {"print", "input", "open", "exec", "eval", "__import__"}
MUTANTES = {
    "append", "extend", "insert", "remove", "pop", "sort", "reverse", "update",
    "clear", "setdefault", "popitem", "add", "discard", "appendleft", "extendleft",
}
EXTERNOS = {
    "now", "today", "utcnow", "random", "randint", "choice", "choices", "shuffle",
    "sample", "uniform", "time", "sleep", "getenv",
}
EXIGIDAS = {nome for funcoes in FUNCOES_POR_FASE.values() for nome in funcoes}


def _viol(funcao, no, regra, mensagem):
    return {"funcao": funcao, "linha": getattr(no, "lineno", 0), "regra": regra, "mensagem": mensagem}


def verificar(codigo):
    """Devolve {'sintaxe': erro|None, 'definidas': [...], 'violacoes': [...]}."""
    try:
        arvore = ast.parse(codigo)
    except SyntaxError as erro:
        return {"sintaxe": f"linha {erro.lineno}: {erro.msg}", "definidas": [], "violacoes": []}

    definidas = {no.name: no for no in arvore.body if isinstance(no, ast.FunctionDef)}
    violacoes = []

    for no in arvore.body:  # código executado ao importar o módulo
        if isinstance(no, ast.Expr) and isinstance(no.value, ast.Call):
            chamada = no.value.func
            if isinstance(chamada, ast.Name) and chamada.id in PROIBIDAS:
                violacoes.append(_viol("(módulo)", no, "efeito_no_modulo",
                                       f"{chamada.id}() executado ao importar; mova para main()"))

    for nome, funcao in definidas.items():
        if nome == "main":
            continue
        for no in ast.walk(funcao):
            if isinstance(no, (ast.Global, ast.Nonlocal)):
                violacoes.append(_viol(nome, no, "global", "usa global/nonlocal"))
            elif isinstance(no, (ast.For, ast.While, ast.AsyncFor)):
                violacoes.append(_viol(nome, no, "laco", "usa laço for/while; prefira comprehension, map, filter ou reduce"))
            elif isinstance(no, ast.AugAssign):
                violacoes.append(_viol(nome, no, "acumulador", "atribuição aumentada (+=, -=...) indica acumulador"))
            elif isinstance(no, (ast.Assign, ast.AnnAssign)):
                alvos = no.targets if isinstance(no, ast.Assign) else [no.target]
                for alvo in alvos:
                    if isinstance(alvo, (ast.Subscript, ast.Attribute)):
                        violacoes.append(_viol(nome, no, "altera_no_lugar", "altera um objeto no lugar (x[k] = v ou x.attr = v)"))
            elif isinstance(no, ast.Delete):
                violacoes.append(_viol(nome, no, "altera_no_lugar", "usa del"))
            elif isinstance(no, ast.Call):
                chamada = no.func
                if isinstance(chamada, ast.Name) and chamada.id in PROIBIDAS:
                    violacoes.append(_viol(nome, no, "efeito", f"usa {chamada.id}() dentro do núcleo"))
                elif isinstance(chamada, ast.Attribute) and chamada.attr in MUTANTES:
                    violacoes.append(_viol(nome, no, "metodo_mutante", f"chama .{chamada.attr}(), que altera o objeto"))
                elif isinstance(chamada, ast.Attribute) and chamada.attr in EXTERNOS:
                    violacoes.append(_viol(nome, no, "externo", f"depende de algo externo (.{chamada.attr}())"))

    preco_final = definidas.get("preco_final")
    if preco_final is not None:
        nomes = {n.id for n in ast.walk(preco_final) if isinstance(n, ast.Name)}
        if "compor" not in nomes:
            violacoes.append(_viol("preco_final", preco_final, "sem_compor",
                                   "preco_final deve usar compor (desconto e depois frete)"))

    return {"sintaxe": None, "definidas": sorted(definidas), "violacoes": violacoes}


def resumo_texto(resultado):
    """Texto simples com as violações, agrupadas por função."""
    if resultado["sintaxe"]:
        return [f"Erro de sintaxe em funcional.py: {resultado['sintaxe']}"]
    linhas = []
    for v in sorted(resultado["violacoes"], key=lambda v: (v["funcao"], v["linha"])):
        marca = "" if v["funcao"] in EXIGIDAS or v["funcao"] == "(módulo)" else " (auxiliar, não pontua)"
        linhas.append(f"  {v['funcao']} (linha {v['linha']}){marca}: {v['mensagem']}")
    return linhas
