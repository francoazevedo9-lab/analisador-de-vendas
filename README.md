# Analisador Automático de Vendas

Script Python que lê uma planilha de vendas em CSV e gera um relatório 
automático completo — tanto no terminal quanto em PDF profissional.

## O que ele faz

- Calcula o total vendido no período
- Identifica o produto mais vendido
- Encontra o melhor dia de vendas
- Mostra o faturamento separado por produto
- Gera um PDF profissional e formatado com todos os dados

## Arquivos

- `analisar.py` — exibe o relatório direto no terminal
- `gerar_relatorio.py` — gera um PDF profissional com os dados
- `vendas.csv` — arquivo de exemplo com dados de vendas

## Como usar

1. Coloque seu arquivo de vendas na mesma pasta
2. O arquivo deve ter as colunas: `data`, `produto`, `quantidade`, `preco_unitario`
3. Para ver no terminal:
```bash
python analisar.py
```
4. Para gerar o PDF:
```bash
python gerar_relatorio.py
```

## Exemplo de resultado — Terminal
```
========================================
   RELATÓRIO DE VENDAS
========================================

Total vendido: R$ 1758.00
Produto mais vendido: Tênis
Melhor dia: 2024-01-12

Vendas por produto:
  Tênis: R$ 799.60
  Camiseta: R$ 598.80
  Calça: R$ 359.60
========================================
```

## Tecnologias

- Python 3
- Pandas
- ReportLab

## Autor

Guilherme Franco — Desenvolvedor Python | Automação e Análise de Dados  
[LinkedIn](https://www.linkedin.com/in/guilherme-franco-de-moraes-azevedo)