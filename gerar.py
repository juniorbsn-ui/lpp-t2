"""Gerador de dados do T2 (Funcional).

Uso:
    python gerar.py SUA_MATRICULA

Cria, na pasta atual, dois arquivos:
    config.json   -> sua configuração (sub-domínio, eixo do relatório, política de desconto)
    pedidos.json  -> seus pedidos
"""
import hashlib
import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

CATALOGOS = {
    "Restaurante": {
        "Pratos": [("Prato executivo", 32.0), ("Feijoada", 45.0), ("Risoto", 38.0)],
        "Bebidas": [("Suco natural", 9.0), ("Refrigerante", 7.0), ("Água", 4.0)],
        "Sobremesas": [("Pudim", 12.0), ("Mousse", 11.0), ("Sorvete", 10.0)],
    },
    "Farmácia": {
        "Medicamentos": [("Analgésico", 14.0), ("Antialérgico", 22.0), ("Vitamina C", 18.0)],
        "Higiene": [("Sabonete", 3.5), ("Shampoo", 19.0), ("Creme dental", 8.0)],
        "Cosméticos": [("Protetor solar", 42.0), ("Hidratante", 36.0), ("Batom", 27.0)],
    },
    "Oficina mecânica": {
        "Peças": [("Filtro de óleo", 35.0), ("Pastilha de freio", 120.0), ("Vela", 28.0)],
        "Serviços": [("Troca de óleo", 90.0), ("Alinhamento", 110.0), ("Balanceamento", 80.0)],
        "Acessórios": [("Tapete", 60.0), ("Capa de volante", 45.0), ("Aromatizante", 12.0)],
    },
    "Livraria": {
        "Livros": [("Romance", 49.0), ("Técnico", 98.0), ("Infantil", 34.0)],
        "Papelaria": [("Caderno", 18.0), ("Caneta", 4.5), ("Agenda", 39.0)],
        "Jogos": [("Quebra-cabeça", 56.0), ("Jogo de cartas", 25.0), ("Tabuleiro", 130.0)],
    },
    "Pet shop": {
        "Alimentos": [("Ração", 89.0), ("Petisco", 15.0), ("Sachê", 4.0)],
        "Higiene": [("Shampoo pet", 24.0), ("Tapete higiênico", 52.0), ("Escova", 16.0)],
        "Brinquedos": [("Bolinha", 8.0), ("Corda", 12.0), ("Mordedor", 14.0)],
    },
    "Loja de informática": {
        "Periféricos": [("Mouse", 45.0), ("Teclado", 120.0), ("Headset", 160.0)],
        "Armazenamento": [("Pendrive", 40.0), ("SSD", 280.0), ("HD externo", 350.0)],
        "Cabos": [("Cabo HDMI", 22.0), ("Cabo USB", 15.0), ("Carregador", 65.0)],
    },
    "Padaria": {
        "Pães": [("Pão francês", 1.2), ("Pão de forma", 9.0), ("Baguete", 7.5)],
        "Doces": [("Bolo", 28.0), ("Cuca", 22.0), ("Sonho", 6.0)],
        "Frios": [("Queijo", 38.0), ("Presunto", 32.0), ("Salame", 45.0)],
    },
    "Material de construção": {
        "Ferramentas": [("Martelo", 35.0), ("Chave de fenda", 14.0), ("Furadeira", 240.0)],
        "Tintas": [("Tinta branca", 110.0), ("Tinta cinza", 115.0), ("Rolo", 18.0)],
        "Elétrica": [("Fio", 65.0), ("Tomada", 9.0), ("Disjuntor", 19.0)],
    },
}
EIXOS = ["cliente", "mes", "categoria"]
POLITICAS = "ABCD"
NOMES = ["Ana", "Bruno", "Carla", "Diego", "Elisa", "Fábio", "Gisele", "Hugo",
         "Iara", "Jonas", "Karen", "Lucas", "Marina", "Nilo", "Olívia", "Paulo"]
SOBRENOMES = ["Silva", "Souza", "Pereira", "Costa", "Müller", "Weber", "Schmitt", "Koch"]


def _hash(texto):
    return hashlib.sha256(texto.encode("utf-8")).digest()


def parametros(matricula):
    """Sub-domínio, eixo do relatório e política de desconto da matrícula."""
    h = _hash(f"t2-2026-2:param:{int(matricula)}")
    subdominios = list(CATALOGOS)
    sub = subdominios[h[0] % len(subdominios)]
    return {
        "matricula": int(matricula),
        "subdominio": sub,
        "eixo": EIXOS[h[1] % len(EIXOS)],
        "politica": POLITICAS[h[2] % len(POLITICAS)],
        "categoria_promocional": next(iter(CATALOGOS[sub])),
    }


def gerar_pedidos(matricula, conjunto="visivel", quantidade=60):
    """Gera os pedidos. 'visivel' é o conjunto que o aluno recebe; os demais são do corretor."""
    h = _hash(f"t2-2026-2:dados:{int(matricula)}:{conjunto}")
    rng = random.Random(int.from_bytes(h[:8], "big"))
    catalogo = CATALOGOS[parametros(matricula)["subdominio"]]
    produtos = [(prod, cat, preco) for cat, lista in catalogo.items() for prod, preco in lista]
    clientes = rng.sample([f"{a} {b}" for a in NOMES for b in SOBRENOMES], 10)
    inicio = date(2026, 3, 1)
    pedidos = []
    for numero in range(1, quantidade + 1):
        itens = [
            {
                "produto": prod,
                "categoria": cat,
                "quantidade": rng.randint(1, 6),
                "preco_unitario": round(preco * rng.choice([0.9, 1.0, 1.1]), 2),
            }
            for prod, cat, preco in rng.sample(produtos, rng.randint(1, 4))
        ]
        pedidos.append({
            "id": numero,
            "cliente": rng.choice(clientes),
            "data": (inicio + timedelta(days=rng.randint(0, 183))).isoformat(),
            "status": rng.choices(["pago", "aberto", "cancelado"], [0.6, 0.2, 0.2])[0],
            "itens": itens,
        })
    return pedidos


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Uso: python gerar.py SUA_MATRICULA")
        sys.exit(1)
    matricula = int(sys.argv[1])
    config = parametros(matricula)
    Path("config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    Path("pedidos.json").write_text(
        json.dumps(gerar_pedidos(matricula), ensure_ascii=False, indent=2), encoding="utf-8")
    print("Arquivos criados: config.json e pedidos.json")
    print(f"  Sub-domínio ........ {config['subdominio']}")
    print(f"  Eixo do relatório .. {config['eixo']}")
    print(f"  Política de desconto {config['politica']}")
    print(f"  Categoria promocional {config['categoria_promocional']} (usada só na política D)")


if __name__ == "__main__":
    main()
