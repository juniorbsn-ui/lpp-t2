# Trabalho 02 — Programação Funcional

**Linguagem de Programação e Paradigmas · UNIDAVI · Sistemas de Informação**
**Prof. Ademar Perfoll Junior**

Você vai construir, em **Python**, o módulo de relatórios e regras de negócio de um **Sistema de Gestão de Pedidos**, usando **programação funcional**: funções puras, dados imutáveis, `map`/`filter`/`reduce`, composição de funções e closures.

A especificação completa está no **[ENUNCIADO.md](ENUNCIADO.md)**. Leia-o antes de começar. Este README é o guia rápido.

- **Prazo:** 10/11/2026
- **Você precisa de:** Python 3.10 ou mais novo, `git` e uma conta no GitHub.

## Passo a passo

**1. Crie o seu repositório a partir deste modelo.**
Clique em **Use this template → Create a new repository**. Dê o nome `lpp-t2-SUA_MATRICULA`, na sua conta, com visibilidade **Public**. Depois clone-o no seu computador:

```
git clone https://github.com/SEU_USUARIO/lpp-t2-SUA_MATRICULA.git
cd lpp-t2-SUA_MATRICULA
```

**2. Gere a sua configuração e os seus dados.**
Os dados e algumas regras mudam de aluno para aluno, a partir da sua matrícula:

```
python gerar.py SUA_MATRICULA
```

Isso cria `config.json` (seu eixo de relatório e sua política de desconto) e `pedidos.json` (seus pedidos). Não os envie ao GitHub: já estão no `.gitignore`.

**3. Implemente as funções em `funcional.py`, fase por fase.**
O arquivo já traz o esqueleto de cada função, com a descrição do que ela deve fazer. Substitua cada `raise NotImplementedError` pela sua implementação.

**4. Confira o seu trabalho a cada passo.**

```
python conferir.py
```

Ele mostra ✓ ou ✗ por função, com o motivo. Rode quantas vezes quiser.

**5. Faça commits pequenos, por fase.**

```
git add funcional.py
git commit -m "fase 2: imutabilidade em aplicar_status"
git push
```

**6. Prepare os arquivos de entrega** (veja a seção *Entrega*).

## As fases

| Fase | O que você implementa | Conceito |
|---|---|---|
| 1 | `total_item`, `total_pedido`, `esta_pago` | Funções puras |
| 2 | `aplicar_status`, `adicionar_item`, `cancelar` | Imutabilidade |
| 3 | `pedidos_pagos`, `faturamento`, `totais_por_eixo`, `top_n` | `map`, `filter`, `reduce` |
| 4 | `criar_regra_desconto`, `aplicar_desconto`, `aplicar_frete`, `compor`, `preco_final` | Ordem superior, closures, composição |
| 5 | `gerar_relatorio` | Pipeline integrado |

Nas Fases 3 e 4, implemente pelo menos o **eixo** e a **política** que aparecem no seu `config.json`.

## Regras do núcleo puro

Todas as funções de `funcional.py`, exceto `main`, formam o **núcleo puro**. Nele:

- **Não use** `global`, `nonlocal`, laços `for`/`while`, `+=`/`-=`, `print`, `input`, `open`, relógio (`datetime.now`) nem aleatoriedade.
- **Não altere** nenhum argumento recebido (`x[k] = v`, `.append`, `.sort`, `.update`, `del`). Devolva valores novos.
- São bem-vindos: comprehensions, `map`, `filter`, `functools.reduce`, `sum`, `sorted`, `min`, `max`, `any`.
- Ler `pedidos.json` e imprimir resultados fica só em `main()` (a "borda").

## Entrega

A entrega é o **seu repositório no GitHub**, que deve ser **público**. Vale o **último commit feito até o prazo**.

Na **raiz** do repositório devem estar:

| Arquivo | O que é |
|---|---|
| `funcional.py` | Suas implementações (obrigatório) |
| `README.md` | **O seu** README de decisões de projeto (veja abaixo) |
| `uso_ia.md` | Registro do uso de IA, preenchido |

**Antes de entregar:**

1. **Troque este README pelo seu.** Substitua todo o conteúdo de `README.md` por um texto seu, com estas quatro seções, escritas com as suas palavras (algumas frases em cada):
   - **Por que cada função do núcleo é pura:** o que torna suas funções puras; dê o exemplo de uma função sua e diga o que ela recebe e devolve.
   - **Onde ficam os efeitos (a borda):** o que o programa lê e imprime, em qual função, e por que isso não está no núcleo.
   - **Decisões de projeto:** escolhas que você fez (comprehension ou `reduce` em cada função, como organizou a política de desconto, como lidou com lista vazia).
   - **O que foi mais difícil:** o que travou você e como resolveu.
2. **Preencha o `uso_ia.md`.** Registre o que pediu à IA, o que aceitou e o que rejeitou ou corrigiu, e por quê. Se não usou IA, escreva isso e explique como estudou.
3. **Dê `git push`** e confira no GitHub que os três arquivos estão na raiz e que o repositório abre sem erro.
4. **Envie o link do seu repositório**, junto com a sua matrícula.


## Avaliação (100 pontos)

| Item | Pontos |
|---|---|
| Fase 1 · Funções puras | 10 |
| Fase 2 · Imutabilidade | 15 |
| Fase 3 · map, filter, reduce | 25 |
| Fase 4 · Ordem superior, closures, composição | 25 |
| Fase 5 · Pipeline integrado | 20 |
| README e uso de IA | 5 |

Em cada fase, **70%** vem do resultado correto e **30%** do estilo funcional. O corretor roda o seu código com os seus dados **e com outros conjuntos que você não vê**, incluindo casos de borda (limites das políticas, lista vazia, ordem embaralhada). Passar no `conferir.py` é necessário, mas não garante a nota máxima.

## Sobre o uso de IA

IA é permitida e deve ser registrada em `uso_ia.md`. O que a avaliação mede é se **você consegue entender, conferir e alterar** o que entregou. Para aprender de verdade: escreva você mesmo 2 ou 3 exemplos de entrada e saída antes de pedir código, peça à IA que **explique** cada função e leia as mensagens do `conferir.py`.

## Arquivos deste repositório

| Arquivo | Para quê |
|---|---|
| `ENUNCIADO.md` | Especificação completa do trabalho |
| `funcional.py` | Esqueleto das funções, para você implementar |
| `gerar.py` | Gera `config.json` e `pedidos.json` a partir da sua matrícula |
| `conferir.py` | Confere o seu código enquanto você trabalha |
| `estilo.py`, `util_t2.py`, `exemplos.json` | Apoio ao `conferir.py` (não precisa editar) |
| `uso_ia.md` | Modelo do registro de uso de IA |

## Dúvidas

Pelo Google Classroom da turma.
