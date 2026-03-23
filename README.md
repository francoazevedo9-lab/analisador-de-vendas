# Analisador Automático de Vendas

Script Python que lê uma planilha de vendas em CSV e gera um relatório automático com os principais indicadores do negócio.

## O que ele faz

- Calcula o total vendido no período
- Identifica o produto mais vendido
- Encontra o melhor dia de vendas
- Mostra o faturamento separado por produto

## Como usar

1. Coloque seu arquivo de vendas no formato CSV na mesma pasta
2. O arquivo deve ter as colunas: `data`, `produto`, `quantidade`, `preco_unitario`
3. Execute o script:
```bash
python analisar.py
```

## Exemplo de resultado
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

## Autor

Guilherme Franco — Desenvolvedor Python | Automação e Análise de Dados