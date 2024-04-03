
import pandas as pd
import streamlit as st
import streamlit_shadcn_ui as ui
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

vendedores = pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/vendedores.csv', delimiter=';')
vendas=pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/venda.csv', delimiter=';', encoding='latin-1')
clientes=pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/clientes.csv', delimiter=';', encoding='latin-1')

# COMISSAO
mesclagem_vendedores = pd.merge(vendedores,vendas[['FVENDEDOR','FCOMISSAO','FDATAEMI','FVALVENDA','IDCLI']],left_on='IDVENDEDOR',right_on='FVENDEDOR')
mesclagem_vendedores = mesclagem_vendedores.drop(columns='IDVENDEDOR')

comissao_venda_vendedor = mesclagem_vendedores.groupby(['FVENDEDOR','NOME'])[['FCOMISSAO','FVALVENDA']].sum().reset_index()
comissao_venda_vendedor_data = mesclagem_vendedores.groupby(['FVENDEDOR','NOME','FDATAEMI'])[['FCOMISSAO','FVALVENDA']].sum().reset_index()

# Selecionar o vendedor
vendedor_selecionado = st.selectbox('Selecione um vendedor:', comissao_venda_vendedor['NOME'])

# Filtrar os dados para o vendedor selecionado
dados_vendedor_selecionado = comissao_venda_vendedor[comissao_venda_vendedor['NOME'] == vendedor_selecionado]
# Criar o gráfico de linhas horizontais
fig = go.Figure()
fig.add_trace(go.Bar(y=['Comissão', 'Valor de Venda'], x=dados_vendedor_selecionado[['FCOMISSAO', 'FVALVENDA']].values[0], orientation='h'))

# Personalizar o layout
fig.update_layout(
    title=f'Desempenho de Vendas de {vendedor_selecionado}',
    xaxis_title="Valor",
    yaxis_title="Tipo",
)

cols = st.columns(4)
with cols[0]:
    st.plotly_chart(fig)
with cols[3]:
    valor_venda_formatado = f'R${dados_vendedor_selecionado["FVALVENDA"].values[0]:,.2f}'
    ui.metric_card(title="VENDAS", content=valor_venda_formatado, description="SOMA DO VALOR DE VENDA DE CADA PRODUTO", key="card2")
    valor_comissao_formatado = f'R${dados_vendedor_selecionado["FCOMISSAO"].values[0]:,.2f}'
    ui.metric_card(title="COMISSAO", content=valor_comissao_formatado, description="SOMA DO VALOR DE VENDA DE CADA PRODUTO", key="card3")

cliente_vendedor = pd.merge(mesclagem_vendedores[['FVENDEDOR','FCOMISSAO','FVALVENDA','IDCLI']],clientes[['IDFORN','NOMEFORN','CP_CIDADE','UF']],left_on='IDCLI',right_on='IDFORN')
cliente_vendedor = pd.merge(cliente_vendedor[['FVENDEDOR','FCOMISSAO','FVALVENDA','IDCLI','IDFORN','NOMEFORN','CP_CIDADE','UF']],vendedores,left_on='FVENDEDOR',right_on='IDVENDEDOR')
colunas_drop=['IDFORN','FVENDEDOR']
cliente_vendedor = cliente_vendedor.drop(columns=colunas_drop)
cliente_vendedor = cliente_vendedor.groupby(['IDCLI','NOMEFORN','CP_CIDADE','UF','IDVENDEDOR','NOME'])[['FVALVENDA','FCOMISSAO']].sum().reset_index()

# Filtrar os dados para o vendedor selecionado
dados_vendedor_selecionado_1 = cliente_vendedor[cliente_vendedor['NOME'] == vendedor_selecionado]

# Criar o gráfico de barras horizontais para os clientes
fig_clientes = go.Figure()
fig_clientes.add_trace(go.Bar(y=dados_vendedor_selecionado_1['NOMEFORN'], x=dados_vendedor_selecionado_1['FVALVENDA'],
                               orientation='h', name='Valor de Venda'))
fig_clientes.add_trace(go.Bar(y=dados_vendedor_selecionado_1['NOMEFORN'], x=dados_vendedor_selecionado_1['FCOMISSAO'],
                               orientation='h', name='Comissão'))

# Personalizar o layout do gráfico
fig_clientes.update_layout(
    title=f'Desempenho de Vendas dos Clientes de {vendedor_selecionado}',
    xaxis_title="Valor",
    yaxis_title="Clientes",
    barmode='relative'
)

cols_1 = st.columns(3)

with cols_1[0]:
    st.plotly_chart(fig_clientes)
with cols_1[2]:
    st.write("Dados dos Clientes:")
    dados_vendedor_selecionado_1 = dados_vendedor_selecionado_1.rename(columns={'IDCLI': 'CODIGO','NOMEFORN':'CLIENTE', 'CP_CIDADE': 'CIDADE','FVALVENDA':'VALOR COMPRA','FCOMISSAO':'COMISSAO'})
    st.dataframe(dados_vendedor_selecionado_1[['CODIGO', 'CLIENTE', 'CIDADE', 'UF', 'VALOR COMPRA', 'COMISSAO']])
