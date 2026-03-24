import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

# Lê os dados
df = pd.read_csv("vendas.csv")
df["total"] = df["quantidade"] * df["preco_unitario"]

# Cálculos
total_geral = df["total"].sum()
produto_top = df.groupby("produto")["total"].sum().idxmax()
melhor_dia = df.groupby("data")["total"].sum().idxmax()
por_produto = df.groupby("produto")["total"].sum().sort_values(ascending=False)

# Cria o PDF
doc = SimpleDocTemplate("relatorio_vendas.pdf", pagesize=A4,
                        rightMargin=2*cm, leftMargin=2*cm,
                        topMargin=2*cm, bottomMargin=2*cm)

styles = getSampleStyleSheet()
azul = colors.HexColor("#1565C0")
azul_claro = colors.HexColor("#E3F2FD")
branco = colors.white

titulo_style = ParagraphStyle("titulo", parent=styles["Title"],
                               fontSize=22, textColor=azul, spaceAfter=6)
sub_style = ParagraphStyle("sub", parent=styles["Normal"],
                            fontSize=11, textColor=colors.grey, spaceAfter=20)
label_style = ParagraphStyle("label", parent=styles["Normal"],
                              fontSize=10, textColor=colors.grey)
valor_style = ParagraphStyle("valor", parent=styles["Normal"],
                              fontSize=18, textColor=azul, fontName="Helvetica-Bold")

elementos = []

# Cabeçalho
elementos.append(Paragraph("Relatório de Vendas", titulo_style))
elementos.append(Paragraph(f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}", sub_style))
elementos.append(Spacer(1, 0.3*cm))

# Cards de resumo
resumo = [
    ["Total Vendido", "Produto Destaque", "Melhor Dia"],
    [f"R$ {total_geral:.2f}", produto_top, melhor_dia]
]
tabela_resumo = Table(resumo, colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
tabela_resumo.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), azul),
    ("TEXTCOLOR", (0,0), (-1,0), branco),
    ("BACKGROUND", (0,1), (-1,1), azul_claro),
    ("TEXTCOLOR", (0,1), (-1,1), azul),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME", (0,1), (-1,1), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,0), 10),
    ("FONTSIZE", (0,1), (-1,1), 14),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("ROWBACKGROUNDS", (0,0), (-1,-1), [azul, azul_claro]),
    ("ROUNDEDCORNERS", [6,6,6,6]),
    ("TOPPADDING", (0,0), (-1,-1), 12),
    ("BOTTOMPADDING", (0,0), (-1,-1), 12),
    ("GRID", (0,0), (-1,-1), 0, branco),
]))
elementos.append(tabela_resumo)
elementos.append(Spacer(1, 0.8*cm))

# Tabela de vendas por produto
elementos.append(Paragraph("Vendas por Produto", ParagraphStyle("sec",
    parent=styles["Heading2"], fontSize=13, textColor=azul, spaceAfter=8)))

dados_tabela = [["Produto", "Total Vendido"]]
for produto, valor in por_produto.items():
    dados_tabela.append([produto, f"R$ {valor:.2f}"])

tabela = Table(dados_tabela, colWidths=[9*cm, 7*cm])
tabela.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), azul),
    ("TEXTCOLOR", (0,0), (-1,0), branco),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 11),
    ("ALIGN", (1,0), (1,-1), "RIGHT"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [branco, azul_claro]),
    ("TOPPADDING", (0,0), (-1,-1), 10),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ("LEFTPADDING", (0,0), (-1,-1), 14),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#BBDEFB")),
]))
elementos.append(tabela)
elementos.append(Spacer(1, 0.8*cm))

# Tabela detalhada
elementos.append(Paragraph("Detalhamento de Vendas", ParagraphStyle("sec2",
    parent=styles["Heading2"], fontSize=13, textColor=azul, spaceAfter=8)))

dados_det = [["Data", "Produto", "Qtd", "Preço Unit.", "Total"]]
for _, row in df.iterrows():
    dados_det.append([
        row["data"], row["produto"],
        str(int(row["quantidade"])),
        f"R$ {row['preco_unitario']:.2f}",
        f"R$ {row['total']:.2f}"
    ])

tabela_det = Table(dados_det, colWidths=[3.5*cm, 4*cm, 2*cm, 3.5*cm, 3.5*cm])
tabela_det.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), azul),
    ("TEXTCOLOR", (0,0), (-1,0), branco),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 10),
    ("ALIGN", (2,0), (-1,-1), "CENTER"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [branco, azul_claro]),
    ("TOPPADDING", (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ("LEFTPADDING", (0,0), (-1,-1), 10),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#BBDEFB")),
]))
elementos.append(tabela_det)

# Rodapé
elementos.append(Spacer(1, 1*cm))
elementos.append(Paragraph("Gerado por Guilherme Franco — Desenvolvedor Python",
    ParagraphStyle("rodape", parent=styles["Normal"],
                   fontSize=9, textColor=colors.grey, alignment=1)))

doc.build(elementos)
print("✅ Relatório gerado: relatorio_vendas.pdf")