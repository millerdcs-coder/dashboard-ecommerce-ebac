# Dashboard Interativo de E-commerce

Este projeto é uma aplicação web interativa construída com Dash e Plotly em Python. O objetivo é visualizar a análise de dados de um e-commerce, explorando relações entre preços, avaliações, descontos e volume de vendas.

## Funcionalidades
- **Painéis Interativos:** Gráficos estáticos e interativos renderizados com Plotly Express.
- **Filtro Dinâmico (Callback):** Um menu suspenso (`dcc.Dropdown`) permite filtrar o gráfico de dispersão (Preço vs Avaliação) em tempo real por Gênero.

## Como rodar o projeto localmente

### 1. Pré-requisitos
Certifique-se de que tem o Python instalado no seu computador. Irá precisar das seguintes bibliotecas:
```bash
pip install dash pandas plotly statsmodels

