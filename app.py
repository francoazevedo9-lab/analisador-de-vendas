import unicodedata
from flask import Flask, request, send_file
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

app = Flask(__name__)

def limpar(texto):
    texto = texto.strip().lower().replace(' ', '_')
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerador de Relatório de Vendas</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: "Segoe UI", sans-serif; background: #0a1628; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .card { background: white; border-radius: 20px; padding: 40px; width: 100%; max-width: 480px; box-shadow: 0 20px 60px rgba(0,0,0,0.4); }
        .logo { text-align: center; margin-bottom: 28px; }
        .logo h1 { color: #1565C0; font-size: 24px; font-weight: 700; margin-bottom: 6px; }
        .logo p { color: #546E7A; font-size: 14px; }
        .upload-area { border: 2px dashed #BBDEFB; border-radius: 12px; padding: 36px 20px; text-align: center; cursor: pointer; transition: all 0.2s; background: #F8FAFF; margin-bottom: 20px; }
        .upload-area:hover { border-color: #1565C0; background: #E3F2FD; }
        .upload-area input { display: none; }
        .upload-icon { font-size: 40px; margin-bottom: 12px; }
        .upload-area h3 { color: #1565C0; font-size: 16px; margin-bottom: 6px; }
        .upload-area p { color: #546E7A; font-size: 13px; }
        .file-name { color: #1565C0; font-size: 13px; font-weight: 600; margin-top: 8px; }
        .btn { width: 100%; padding: 14px; background: #1565C0; color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
        .btn:hover { background: #0D47A1; }
        .btn:disabled { background: #BBDEFB; cursor: not-allowed; }
        .info { background: #E3F2FD; border-radius: 10px; padding: 14px; margin-bottom: 20px; font-size: 13px; color: #1565C0; }
        .info b { display: block; margin-bottom: 4px; }
        .loading { display: none; text-align: center; color: #1565C0; margin-top: 12px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="logo">
            <h1>📊 Gerador de Relatório</h1>
            <p>Suba sua planilha e receba um PDF profissional</p>
        </div>
        <div class="info">
            <b>Como usar:</b>
            Suba sua planilha Excel com as colunas: <b>data, produto, quantidade, preco_unitario</b>
        </div>
        <form method="POST" action="/gerar" enctype="multipart/form-data" onsubmit="mostrarLoading()">
            <div class="upload-area" onclick="document.getElementById('arquivo').click()">
                <div class="upload-icon">📂</div>
                <h3>Clique para selecionar</h3>
                <p>Arquivos .xlsx ou .csv</p>
                <div class="file-name" id="nome-arquivo"></div>
                <input type="file" id="arquivo" name="arquivo" accept=".xlsx,.csv" onchange="mostrarNome(this)">
            </div>
            <button type="submit" class="btn" id="btn-gerar">Gerar Relatório PDF</button>
            <div class="loading" id="loading">⏳ Gerando seu relatório...</div>
        </form>
    </div>
    <script>
        function mostrarNome(input) {
            if (input.files[0]) {
                document.getElementById("nome-arquivo").textContent = "✓ " + input.files[0].name;
            }
        }
        function mostrarLoading() {
            document.getElementById("btn-gerar").disabled = true;
            document.getElementById("loading").style.display = "block";
        }
    </script>
</body>
</html>
'''

@app.route('/gerar', methods=['POST'])
def gerar():
    arquivo = request.files['arquivo']
    nome = arquivo.filename

    if nome.endswith('.xlsx'):
        df = pd.read_excel(arquivo, skiprows=3)
    else:
        df = pd.read_csv(arquivo)

    df.columns = [limpar(c) for c in df.columns]
    print("Colunas:", df.columns.tolist())

    df = df.dropna(subset=['produto'])
    df = df[df['produto'].astype(str).str.strip() != '']
    df['total'] = df['quantidade'] * df['preco_unitario']

    total_geral = df['total'].sum()
    produto_top = df.groupby('produto')['total'].sum().idxmax()
    melhor_dia = df.groupby('data')['total'].sum().idxmax()
    por_produto = df.groupby('produto')['total'].sum().sort_values(ascending=False)

    azul = colors.HexColor("#1565C0")
    azul_claro = colors.HexColor("#E3F2FD")
    branco = colors.white

    pdf_path = 'relatorio_gerado.pdf'
    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("Relatório de Vendas",
        ParagraphStyle("t", parent=styles["Title"], fontSize=22, textColor=azul, spaceAfter=6)))
    elementos.append(Paragraph(f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
        ParagraphStyle("s", parent=styles["Normal"], fontSize=11, textColor=colors.grey, spaceAfter=20)))
    elementos.append(Spacer(1, 0.3*cm))

    resumo = [
        ["Total Vendido", "Produto Destaque", "Melhor Dia"],
        [f"R$ {total_geral:.2f}", produto_top, str(melhor_dia)[:10]]
    ]
    tab_resumo = Table(resumo, colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
    tab_resumo.setStyle(TableStyle([
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
        ("TOPPADDING", (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12),
        ("GRID", (0,0), (-1,-1), 0, branco),
    ]))
    elementos.append(tab_resumo)
    elementos.append(Spacer(1, 0.8*cm))

    elementos.append(Paragraph("Vendas por Produto",
        ParagraphStyle("sec", parent=styles["Heading2"], fontSize=13, textColor=azul, spaceAfter=8)))

    dados_prod = [["Produto", "Total Vendido"]]
    for produto, valor in por_produto.items():
        dados_prod.append([produto, f"R$ {valor:.2f}"])

    tab_prod = Table(dados_prod, colWidths=[9*cm, 7*cm])
    tab_prod.setStyle(TableStyle([
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
    elementos.append(tab_prod)
    elementos.append(Spacer(1, 0.8*cm))

    elementos.append(Paragraph("Detalhamento de Vendas",
        ParagraphStyle("sec2", parent=styles["Heading2"], fontSize=13, textColor=azul, spaceAfter=8)))

    dados_det = [["Data", "Produto", "Qtd", "Preço Unit.", "Total"]]
    for _, row in df.iterrows():
        dados_det.append([
            str(row['data'])[:10], row['produto'],
            str(int(row['quantidade'])),
            f"R$ {row['preco_unitario']:.2f}",
            f"R$ {row['total']:.2f}"
        ])

    tab_det = Table(dados_det, colWidths=[3.5*cm, 4*cm, 2*cm, 3.5*cm, 3.5*cm])
    tab_det.setStyle(TableStyle([
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
    elementos.append(tab_det)

    elementos.append(Spacer(1, 1*cm))
    elementos.append(Paragraph("Gerado por Guilherme Franco — Desenvolvedor Python",
        ParagraphStyle("rod", parent=styles["Normal"], fontSize=9,
                       textColor=colors.grey, alignment=1)))

    doc.build(elementos)
    return send_file(pdf_path, as_attachment=True, download_name='relatorio_vendas.pdf')

if __name__ == '__main__':
    app.run(debug=True)