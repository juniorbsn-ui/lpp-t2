"""Confere o seu funcional.py enquanto você trabalha.

Uso (na pasta do trabalho):
    python gerar.py SUA_MATRICULA     # uma vez, cria config.json e pedidos.json
    python conferir.py

O que ele confere:
  1. Estilo funcional (análise estática): sem laços, global, acumuladores etc.
  2. Pureza e imutabilidade, chamando suas funções duas vezes com os seus dados.
  3. Exemplos pequenos com resposta conhecida (para a sua política e o seu eixo).

A correção final usa outros dados e testes que você não vê. Passar aqui é necessário, mas não garante a nota máxima.
"""
import json
import sys
from pathlib import Path

import estilo
from util_t2 import (FUNCOES_POR_FASE, NOMES_FASES, carregar_modulo, executar_caso, iguais)

PASTA = Path(__file__).resolve().parent


def ler_json(nome):
    caminho = PASTA / nome
    if not caminho.exists():
        sys.exit(f"Não encontrei {nome}. Rode primeiro: python gerar.py SUA_MATRICULA")
    return json.loads(caminho.read_text(encoding="utf-8"))


def casos_dos_seus_dados(pedidos, config):
    """Casos que só conferem pureza e imutabilidade (sem resposta conhecida)."""
    p = pedidos[0]
    novo_item = {"produto": "X", "categoria": "Y", "quantidade": 1, "preco_unitario": 9.9}
    chamadas = [
        (1, "total_item", [p["itens"][0]]), (1, "total_pedido", [p]), (1, "esta_pago", [p]),
        (2, "aplicar_status", [p, "pago"]), (2, "adicionar_item", [p, novo_item]), (2, "cancelar", [p]),
        (3, "pedidos_pagos", [pedidos]), (3, "faturamento", [pedidos]),
        (3, "totais_por_eixo", [pedidos, config["eixo"]]), (3, "top_n", [{"a": 1.0, "b": 2.0, "c": 2.0}, 2]),
        (4, "aplicar_frete", [123.45]),
        (5, "gerar_relatorio", [pedidos, config]),
    ]
    casos = [{"kind": "call", "fase": f, "funcao": n, "args": a, "esperado": None} for f, n, a in chamadas]
    casos.append({"kind": "regra", "fase": 4, "funcao": "criar_regra_desconto",
                  "args": [config["politica"], pedidos, config["categoria_promocional"]], "esperado": None})
    casos.append({"kind": "aplicar_desconto", "fase": 4, "funcao": "aplicar_desconto", "args": [p, 0.1], "esperado": None})
    casos.append({"kind": "preco_final", "fase": 4, "funcao": "preco_final", "args": [p, 0.1], "esperado": None})
    casos.append({"kind": "compor", "fase": 4, "funcao": "compor", "args": ["inc", "dobro", 5], "esperado": 11})
    return casos


def casos_dos_exemplos(exemplos, config):
    casos = []
    for g in exemplos["gerais"]:
        fase = g.get("fase") or next(f for f, fs in FUNCOES_POR_FASE.items() if g["funcao"] in fs)
        casos.append({"kind": "call", "fase": fase, "funcao": g["funcao"], "args": g["args"], "esperado": g["esperado"]})
    v = exemplos["variantes"][f"{config['politica']}|{config['eixo']}"]
    pedidos = exemplos["pedidos"]
    casos.append({"kind": "regra", "fase": 4, "funcao": "criar_regra_desconto",
                  "args": [config["politica"], pedidos, "X"], "esperado": v["taxas"]})
    casos.append({"kind": "call", "fase": 3, "funcao": "totais_por_eixo", "args": [pedidos, config["eixo"]], "esperado": v["totais_por_eixo"]})
    casos.append({"kind": "call", "fase": 5, "funcao": "gerar_relatorio", "args": [pedidos, v["config"]], "esperado": v["relatorio"]})
    return casos


def main():
    config = ler_json("config.json")
    pedidos = ler_json("pedidos.json")
    exemplos = ler_json("exemplos.json")
    arquivo = PASTA / "funcional.py"
    if not arquivo.exists():
        sys.exit("Não encontrei funcional.py nesta pasta.")

    print(f"Configuração: {config['subdominio']} | eixo '{config['eixo']}' | política {config['politica']}\n")
    estatico = estilo.verificar(arquivo.read_text(encoding="utf-8"))
    if estatico["sintaxe"]:
        sys.exit(f"Erro de sintaxe em funcional.py: {estatico['sintaxe']}")
    try:
        modulo = carregar_modulo(arquivo)
    except Exception as erro:  # noqa: BLE001
        sys.exit(f"Não consegui importar funcional.py: {type(erro).__name__}: {erro}")

    violacoes = {}
    for v in estatico["violacoes"]:
        violacoes.setdefault(v["funcao"], []).append(v)

    casos = casos_dos_seus_dados(pedidos, config) + casos_dos_exemplos(exemplos, config)
    por_funcao = {}
    for caso in casos:
        r = executar_caso(modulo, caso)
        info = por_funcao.setdefault(caso["funcao"], {"msgs": [], "ok": 0, "total": 0})
        info["total"] += 1
        if "erro" in r:
            info["msgs"].append(f"erro: {r['erro']}")
            continue
        problemas = []
        if r["mutou"]:
            problemas.append("altera os argumentos recebidos (imutabilidade)")
        if r["impura"]:
            problemas.append("a mesma entrada deu resultados diferentes (pureza)")
        if caso["esperado"] is not None and not iguais(r["r1"], caso["esperado"]):
            problemas.append(f"exemplo: esperado {json.dumps(caso['esperado'], ensure_ascii=False)[:120]}"
                             f" mas obteve {json.dumps(r['r1'], ensure_ascii=False)[:120]}")
        if problemas:
            info["msgs"].extend(problemas)
        else:
            info["ok"] += 1

    fases_ok = 0
    fases_conferidas = 0
    for fase, funcoes in FUNCOES_POR_FASE.items():
        print(f"Fase {fase} — {NOMES_FASES[fase]}")
        fase_ok = True
        for nome in funcoes:
            info = por_funcao.get(nome, {"msgs": [], "ok": 0, "total": 0})
            problemas = list(dict.fromkeys(info["msgs"]))
            problemas += [f"estilo (linha {v['linha']}): {v['mensagem']}" for v in violacoes.get(nome, [])]
            if problemas:
                fase_ok = False
                print(f"  ✗ {nome}")
                for p in problemas[:4]:
                    print(f"      {p}")
            else:
                print(f"  ✓ {nome}")
        fases_conferidas += 1
        fases_ok += fase_ok
        print()

    avisos = [v for nome, lista in violacoes.items() if nome not in {f for fs in FUNCOES_POR_FASE.values() for f in fs}
              for v in lista]
    if avisos:
        print("Avisos em funções auxiliares (não pontuam, mas valem atenção):")
        for v in avisos:
            print(f"  {v['funcao']} (linha {v['linha']}): {v['mensagem']}")
        print()

    print(f"Resumo: {fases_ok} de {fases_conferidas} fases sem problemas nesta conferência.")
    try:
        relatorio = modulo.gerar_relatorio(pedidos, config)
        print("\nRelatório dos seus dados (confira se faz sentido):")
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    except Exception:  # noqa: BLE001
        pass


if __name__ == "__main__":
    main()
