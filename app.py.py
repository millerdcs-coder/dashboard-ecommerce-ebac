import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# 1. LER OS DADOS
df = pd.read_csv('ecommerce_estatistica.csv')

# 2. GRÁFICOS ESTÁTICOS (Os que não mudam com o botão)
fig_hist = px.histogram(df, x='Preço', nbins=20, title='Distribuição de Preços dos Produtos', color_discrete_sequence=['skyblue'])

colunas_numericas = ['Nota', 'N_Avaliações', 'Desconto', 'Preço', 'Qtd_Vendidos_Cod']
correlacao = df[colunas_numericas].corr()
fig_heatmap = px.imshow(correlacao, text_auto=".2f", aspect="auto", title='Mapa de Calor: Correlação', color_continuous_scale='RdBu_r')

df_marcas = df['Marca'].value_counts().reset_index().head(10)
df_marcas.columns = ['Marca', 'Quantidade']
fig_bar = px.bar(df_marcas, x='Quantidade', y='Marca', orientation='h', title='Top 10 Marcas', color_discrete_sequence=['#2ca02c'])
fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}) 

fig_pie = px.pie(df, names='Gênero', title='Distribuição por Gênero')
fig_density = px.histogram(df, x='Desconto', histnorm='probability density', title='Densidade de Desconto', color_discrete_sequence=['salmon'])
fig_reg = px.scatter(df, x='Preço', y='Qtd_Vendidos_Cod', trendline='ols', title='Regressão: Preço vs Vendas', trendline_color_override='red')

# 3. CONSTRUIR O LAYOUT DA APLICAÇÃO (Com o Dropdown)
app = dash.Dash(__name__)

app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'padding': '20px'}, children=[
    
    html.H1("Dashboard Interativo de E-commerce", style={'textAlign': 'center', 'color': '#333'}),
    html.P("Análise de vendas, preços e avaliações de produtos.", style={'textAlign': 'center'}),
    
    # Menu interativo para o utilizador
    html.Div([
        html.Label("Filtre o gráfico de dispersão por Gênero:"),
        dcc.Dropdown(
            id='filtro-genero',
            options=[{'label': 'Todos', 'value': 'Todos'}] + [{'label': i, 'value': i} for i in df['Gênero'].unique()],
            value='Todos',
            clearable=False
        )
    ], style={'width': '40%', 'margin': '0 auto', 'paddingBottom': '20px'}),
    
    html.Hr(),
    
    html.Div([
        dcc.Graph(figure=fig_hist, style={'width': '48%', 'display': 'inline-block'}),
        # Este gráfico vai receber a atualização dinâmica
        dcc.Graph(id='grafico-dispersao-dinamico', style={'width': '48%', 'display': 'inline-block'}),
    ]),
    
    html.Div([
        dcc.Graph(figure=fig_heatmap, style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(figure=fig_bar, style={'width': '48%', 'display': 'inline-block'}),
    ]),

    html.Div([
        dcc.Graph(figure=fig_pie, style={'width': '32%', 'display': 'inline-block'}),
        dcc.Graph(figure=fig_density, style={'width': '32%', 'display': 'inline-block'}),
        dcc.Graph(figure=fig_reg, style={'width': '32%', 'display': 'inline-block'}),
    ])
])

# 4. A LÓGICA DE INTERATIVIDADE (O CALLBACK)
@app.callback(
    Output('grafico-dispersao-dinamico', 'figure'),
    Input('filtro-genero', 'value')
)
def atualizar_grafico_dispersao(genero_selecionado):
    if genero_selecionado == 'Todos':
        df_filtrado = df
    else:
        df_filtrado = df[df['Gênero'] == genero_selecionado]
    
    fig = px.scatter(df_filtrado, x='Preço', y='Nota', title=f'Preço vs Avaliação ({genero_selecionado})',
                     color_discrete_sequence=['purple'], opacity=0.7)
    return fig

# 5. EXECUTAR O SERVIDOR LOCALMENTE NO SEU COMPUTADOR
if __name__ == '__main__':
    app.run(debug=True)
