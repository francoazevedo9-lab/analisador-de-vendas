import pandas as pd

# Lê o arquivo de vendas
df = pd.read_csv("vendas.csv")

# Calcula o total de cada venda
df["total"] = df["quantidade"] * df["preco_unitario"]

# Gera o relatório
print("=" * 40)
print("   RELATÓRIO DE VENDAS")
print("=" * 40)

total_geral = df["total"].sum()
print(f"\nTotal vendido: R$ {total_geral:.2f}")

produto_top = df.groupby("produto")["total"].sum().idxmax()
print(f"Produto mais vendido: {produto_top}")

melhor_dia = df.groupby("data")["total"].sum().idxmax()
print(f"Melhor dia: {melhor_dia}")

print("\nVendas por produto:")
por_produto = df.groupby("produto")["total"].sum().sort_values(ascending=False)
for produto, valor in por_produto.items():
    print(f"  {produto}: R$ {valor:.2f}")

print("\n" + "=" * 40)