# Trabalho 02 — Programação Funcional

**Disciplina:** Linguagem de Programação e Paradigmas · **Linguagem:** Python (3.10 ou mais novo)
**Prazo:** 10/11/2026 · **Entrega:** repositório no GitHub (veja a seção 6)

## 1. Contexto

Você faz parte da equipe do **Sistema de Gestão de Pedidos** de uma empresa. Sua tarefa é construir o **módulo de relatórios e regras de negócio** no estilo funcional: funções puras, dados imutáveis, `map`/`filter`/`reduce`, composição de funções e closures.

O trabalho é uma **trilha de 5 fases**. Cada fase trabalha um conceito da aula e termina com uma conferência automática. Os dados e algumas regras mudam de aluno para aluno, a partir da sua matrícula.

## 2. Como começar

1. Crie o seu repositório no GitHub, chamado `lpp-t2-SUA_MATRICULA`, a partir do modelo https://github.com/juniorbsn-ui/lpp-t2 (ou crie um repositório vazio e copie nele os arquivos do kit). Clone-o no seu computador.
2. Gere a sua configuração e os seus dados (use a sua matrícula):
   ```
   python gerar.py SUA_MATRICULA
   ```
   Isso cria `config.json` (seu sub-domínio, o eixo do seu relatório e a sua política de desconto) e `pedidos.json` (seus pedidos).
3. Abra `funcional.py` e implemente as funções, fase por fase.
4. Rode `python conferir.py` quantas vezes quiser. Ele mostra ✓ ou ✗ por função, com o motivo.
5. Troque o `README.md` do repositório pelo seu (seções descritas no `README.md` do kit), preencha `uso_ia.md`, dê `git push` e informe a URL do repositório (seção 6).

## 3. Regras do núcleo (o que o corretor verifica)

Todas as funções de `funcional.py`, exceto `main`, formam o **núcleo puro**. Nele:

- **Não use** `global`, `nonlocal`, laços `for`/`while`, `+=`/`-=` (acumuladores), `print`, `input`, `open`, relógio (`datetime.now`) nem aleatoriedade.
- **Não altere** nenhum argumento recebido: nada de `x[k] = v`, `.append`, `.sort`, `.update`, `del`. Devolva valores novos.
- Comprehensions, `map`, `filter`, `functools.reduce`, `sum`, `sorted`, `min`, `max` e `any` são bem-vindos.
- Ler `pedidos.json` e imprimir resultados faz parte da **borda**: fica só em `main()`.

Uma função **pura** devolve sempre o mesmo resultado para a mesma entrada e não altera nada fora dela.

## 4. Os dados

Um pedido é um dicionário:

```
{"id": 1, "cliente": "Ana Silva", "data": "2026-04-02", "status": "pago",
 "itens": [{"produto": "Caderno", "categoria": "Papelaria", "quantidade": 2, "preco_unitario": 18.0}]}
```

`status` é `"pago"`, `"aberto"` ou `"cancelado"`. Valores em reais, **arredondados a 2 casas** (`round(x, 2)`).

## 5. As fases

### Fase 1 — Funções puras
`total_item(item)`, `total_pedido(pedido)`, `esta_pago(pedido)`.

### Fase 2 — Imutabilidade
`aplicar_status(pedido, novo_status)`, `adicionar_item(pedido, item)`, `cancelar(pedido)`. Todas devolvem um **pedido novo**; o original não pode mudar.

### Fase 3 — map, filter e reduce
- `pedidos_pagos(pedidos)`: lista dos pagos, na mesma ordem.
- `faturamento(pedidos)`: soma dos totais dos pedidos pagos.
- `totais_por_eixo(pedidos, eixo)`: dicionário `{chave: total}` só com pedidos pagos.
  - `"cliente"`: chave é o cliente, total é a soma dos totais dos pedidos.
  - `"mes"`: chave é `"AAAA-MM"` (da data), total é a soma dos totais dos pedidos.
  - `"categoria"`: chave é a categoria do item, total é a soma dos totais dos **itens**.
  - Implemente pelo menos o **eixo do seu `config.json`**.
- `top_n(totais, n)`: lista de `[chave, total]` dos `n` maiores, do maior para o menor; empate: ordem alfabética da chave.

### Fase 4 — Ordem superior, closures e composição
- `criar_regra_desconto(politica, pedidos, categoria_promocional=None)`: devolve uma **função** `regra(pedido)` que dá a taxa de desconto (ex.: `0.05`). Implemente pelo menos a **política do seu `config.json`**:

  | Política | Regra |
  |---|---|
  | A | total do pedido ≥ 500: `0.10`; ≥ 200: `0.05`; senão `0.0` |
  | B | unidades do pedido (soma das quantidades) ≥ 10: `0.08`; ≥ 5: `0.04`; senão `0.0` |
  | C | cliente com **4 ou mais pedidos pagos** na lista `pedidos`: `0.07` em todos os pedidos dele; senão `0.0` |
  | D | pedido com **ao menos um item** da `categoria_promocional`: `0.06`; senão `0.0` |

  *Closure:* a função devolvida "lembra" dados do lugar onde foi criada (a lista `pedidos`, a categoria...). Isso é o que torna a política configurável sem variável global.
- `aplicar_desconto(pedido, regra)`: devolve um pedido **novo** com as chaves `"desconto"` (a taxa) e `"total_com_desconto"` (total do pedido × (1 − taxa), 2 casas).
- `aplicar_frete(valor)`: valor ≥ 300: frete grátis (devolve o valor); abaixo disso, soma 25.
- `compor(f, g)`: devolve a função `x -> f(g(x))`.
- `preco_final(pedido, regra)`: aplica o desconto e **depois** o frete. **Use `compor`.**

### Fase 5 — Pipeline integrado
`gerar_relatorio(pedidos, config)` devolve um dicionário com:

| Chave | Valor |
|---|---|
| `faturamento_bruto` | faturamento dos pedidos pagos |
| `faturamento_final` | soma de `preco_final` dos pedidos pagos, com a política de `config["politica"]` |
| `top3` | `top_n` dos totais por `config["eixo"]`, com n = 3 |
| `ticket_medio` | `faturamento_bruto` ÷ quantidade de pagos (0.0 se não houver pagos) |
| `cancelados` | quantidade de pedidos cancelados |

## 6. Entrega (GitHub)

**O que entregar** — na **raiz** do repositório:

- `funcional.py` (obrigatório)
- `README.md`: **o seu** (substitua o README do kit; as seções estão descritas nele): por que cada função do núcleo é pura, onde ficam os efeitos e quais foram suas decisões
- `uso_ia.md`: registro do uso de IA (veja a seção 8)

**Como entregar:**

1. O repositório deve ser **público**, para o professor poder acessá-lo.
2. A entrega é o próprio repositório no GitHub: envie o **link do seu repositório**, junto com a sua matrícula.
3. Vale o **último commit feito até o prazo**. O que for enviado depois não conta.
4. Trabalhe em **commits pequenos**, por fase, com mensagens que digam o que mudou (por exemplo, "fase 2: imutabilidade em aplicar_status"). O histórico pode ser consultado, e um único commit com tudo pronto na véspera é motivo de conversa.
5. Antes de entregar, confira no GitHub que `funcional.py`, `README.md` e `uso_ia.md` estão na raiz e que o repositório abre sem erro.

## 7. Avaliação (100 pontos)

| Item | Pontos |
|---|---|
| Fase 1 · Funções puras | 10 |
| Fase 2 · Imutabilidade | 15 |
| Fase 3 · map, filter, reduce | 25 |
| Fase 4 · Ordem superior, closures, composição | 25 |
| Fase 5 · Pipeline integrado | 20 |
| README e uso de IA | 5 |

Em cada fase, **70%** vem do resultado correto e **30%** do estilo funcional (pureza, imutabilidade, sem laços e acumuladores).

O corretor roda o seu código com **os seus dados e outros conjuntos que você não vê**, incluindo casos de borda (limites das políticas, lista vazia, ordem embaralhada). Resolver só o exemplo não basta.

## 8. Sobre o uso de IA

Você pode usar IA. O que a avaliação mede é se **você consegue entender, conferir e alterar** o que entregou:

- O corretor pega o que a IA costuma errar: laços com acumulador, alterar a entrada, regras nos limites (`>` no lugar de `>=`).
- O `uso_ia.md` vale pontos: registre o que pediu, o que aceitou e **o que rejeitou ou corrigiu, e por quê**.

Para aprender de verdade: antes de pedir código, escreva você mesmo 2 ou 3 exemplos de entrada e saída; peça à IA que **explique** cada função; rode `conferir.py` a cada passo e leia as mensagens.

Dúvidas sobre o enunciado: pelo Google Classroom da turma.
