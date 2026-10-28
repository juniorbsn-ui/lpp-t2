"""Trabalho 02 - Programação Funcional (Sistema de Gestão de Pedidos).

Implemente as funções abaixo no NÚCLEO PURO deste arquivo.
Regras do núcleo (tudo, exceto main): sem global, sem laços for/while, sem +=,
sem alterar objetos recebidos, sem print/input/open e sem depender do relógio ou de aleatoriedade.
Leitura de arquivos e impressão ficam só em main() (a "borda").

Um pedido é um dicionário:
    {"id": 1, "cliente": "Ana Silva", "data": "2026-04-02", "status": "pago",
     "itens": [{"produto": "...", "categoria": "...", "quantidade": 2, "preco_unitario": 10.5}]}
status: "pago", "aberto" ou "cancelado". Valores em reais, arredondados a 2 casas.

Leia o ENUNCIADO.md para as regras de negócio. Rode `python conferir.py` com frequência.
"""
from functools import reduce  # noqa: F401  (pode usar)


# ---------------------------------------------------------------- Fase 1: funções puras
def total_item(item):
    """quantidade * preco_unitario, arredondado a 2 casas."""
    raise NotImplementedError


def total_pedido(pedido):
    """Soma dos totais dos itens do pedido, arredondada a 2 casas."""
    raise NotImplementedError


def esta_pago(pedido):
    """True se o status do pedido for "pago"."""
    raise NotImplementedError


# ---------------------------------------------------------------- Fase 2: imutabilidade
def aplicar_status(pedido, novo_status):
    """Devolve um pedido NOVO com o status trocado. O original não pode mudar."""
    raise NotImplementedError


def adicionar_item(pedido, item):
    """Devolve um pedido NOVO com o item acrescentado ao final de "itens"."""
    raise NotImplementedError


def cancelar(pedido):
    """Devolve um pedido NOVO com status "cancelado"."""
    raise NotImplementedError


# ---------------------------------------------------------------- Fase 3: map, filter, reduce
def pedidos_pagos(pedidos):
    """Lista com os pedidos pagos, na mesma ordem da entrada."""
    raise NotImplementedError


def faturamento(pedidos):
    """Soma dos totais dos pedidos pagos (arredondada a 2 casas). Lista sem pagos: 0.0."""
    raise NotImplementedError


def totais_por_eixo(pedidos, eixo):
    """Dicionário {chave: total} considerando só pedidos pagos.

    eixo "cliente":   chave = cliente,          total = soma dos totais dos pedidos
    eixo "mes":       chave = "AAAA-MM" da data, total = soma dos totais dos pedidos
    eixo "categoria": chave = categoria do item, total = soma dos totais dos itens
    Implemente pelo menos o eixo da sua configuração (config.json).
    """
    raise NotImplementedError


def top_n(totais, n):
    """Lista de [chave, total] dos n maiores totais, do maior para o menor.
    Empate: ordem alfabética da chave."""
    raise NotImplementedError


# ---------------------------------------------------------------- Fase 4: ordem superior, closures, composição
def criar_regra_desconto(politica, pedidos, categoria_promocional=None):
    """Devolve uma FUNÇÃO regra(pedido) -> taxa de desconto (0.0 a 1.0), conforme a política.

    Implemente pelo menos a política da sua configuração (A, B, C ou D); veja o ENUNCIADO.md.
    """
    raise NotImplementedError


def aplicar_desconto(pedido, regra):
    """Devolve um pedido NOVO com duas chaves a mais:
    "desconto" (taxa dada por regra(pedido)) e "total_com_desconto" (total_pedido * (1 - taxa), 2 casas)."""
    raise NotImplementedError


def aplicar_frete(valor):
    """valor >= 300: frete grátis (devolve o valor). Abaixo disso, soma 25. Arredonde a 2 casas."""
    raise NotImplementedError


def compor(f, g):
    """Devolve uma função x -> f(g(x))."""
    raise NotImplementedError


def preco_final(pedido, regra):
    """Preço final do pedido: aplica o desconto e DEPOIS o frete. Use compor."""
    raise NotImplementedError


# ---------------------------------------------------------------- Fase 5: pipeline integrado
def gerar_relatorio(pedidos, config):
    """Devolve um dicionário com:
    "faturamento_bruto": faturamento dos pedidos pagos
    "faturamento_final": soma de preco_final dos pedidos pagos (política de config["politica"])
    "top3": top_n dos totais por config["eixo"], com n = 3
    "ticket_medio": faturamento_bruto / quantidade de pagos (0.0 se não houver pagos), 2 casas
    "cancelados": quantidade de pedidos cancelados
    """
    raise NotImplementedError


# ---------------------------------------------------------------- Borda (pode usar print/open aqui)
def main():
    import json
    pedidos = json.load(open("pedidos.json", encoding="utf-8"))
    config = json.load(open("config.json", encoding="utf-8"))
    print(json.dumps(gerar_relatorio(pedidos, config), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
