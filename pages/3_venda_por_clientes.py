import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit_shadcn_ui as ui
import pygwalker as pyg
st.set_page_config(layout="wide")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Carregando os dados
compra_itens = pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/compra_itens.csv', delimiter=';')
produtos = pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/produto.csv', delimiter=';', encoding='latin-1')
compras = pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/compra.csv', sep=';', encoding='latin1')
fornecedores = pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/fornecedores.csv', sep=';', encoding='latin1')
vendas=pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/venda.csv', delimiter=';', encoding='latin-1')
venda_itens = pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/venda_itens.csv', delimiter=';', encoding='latin1')
clientes=pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/clientes.csv', delimiter=';', encoding='latin-1')

# Mesclando as tabelas vendas e clientes
venda_cliente = pd.merge(vendas[['FLOJA','IDPEDIDO','IDCLI','SI_CAIXA','FDATAEMI','HORA','FVALVENDA']],clientes[['IDFORN','NOMEFORN']],how='left',left_on='IDCLI',right_on='IDFORN')
venda_cliente.rename(columns= {'NOMEFORN': 'NOMECLI'},inplace=True)
venda_cliente.drop('IDFORN', axis='columns')

# Substituindo NaN por Consumidor Final
venda_cliente['NOMECLI'].fillna('Consumidor Final', inplace=True)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#TELA DE CLIENTES QUE MAIS COMPRARAM

# Agrupando e somando os valores de vendas para cada cliente
clientes_que_mais_comprou = venda_cliente.groupby('IDCLI')['FVALVENDA'].sum().reset_index()

# Ordenando os clientes pelo valor total de vendas em ordem decrescente
clientes_que_mais_comprou = clientes_que_mais_comprou.sort_values(by='FVALVENDA', ascending=False)

# Realizando o merge com a tabela de clientes
tabela_clientes_mais_compraram = pd.merge(clientes_que_mais_comprou[['IDCLI', 'FVALVENDA']],clientes[['IDFORN', 'NOMEFORN', 'UF']],left_on='IDCLI', right_on='IDFORN', how='left')
tabela_clientes_mais_compraram = tabela_clientes_mais_compraram.dropna(subset=['NOMEFORN'])
tabela_clientes_mais_compraram.drop(['IDFORN'], axis=1)


tabela_clientes_mais_compraram = tabela_clientes_mais_compraram.sort_values(by='FVALVENDA', ascending=False)

alteracao_colunas = ['IDCLI','NOMEFORN','UF','FVALVENDA',]
tabela_clientes_mais_compraram = tabela_clientes_mais_compraram.reindex(columns=alteracao_colunas)
# ---------------- GRAFICO FORNECEDORES ----------------------

# Criando o gráfico com Plotly Express
fig = px.bar(tabela_clientes_mais_compraram, x='FVALVENDA', y='NOMEFORN', color='UF', text='IDCLI', orientation='h')

# Personalizando o layout do gráfico
fig.update_layout(
    title="Vendas por Cliente",
    xaxis_title="Soma das Vendas",
    yaxis_title="Cliente",
    legend_title="Estado",
    yaxis={'categoryorder':'total ascending'} # Ordenando os fornecedores da maior para a menor venda
)

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig)
# --------------------- PESQUISA DO NOME DO FORNECEDOR --------------------------
# Formatar FVALVENDA para moeda (Real)
tabela_clientes_mais_compraram['FVALVENDA'] = tabela_clientes_mais_compraram['FVALVENDA'].map(lambda x: f'R$ {x:,.2f}')

# Formatar IDCLI para número inteiro sem vírgulas
tabela_clientes_mais_compraram['IDCLI'] = tabela_clientes_mais_compraram['IDCLI'].map(lambda x: f'{x:}')


search_term = st.text_input("Digite o termo de pesquisa:")

# Filtrando os dados com base no termo de pesquisa
filtered_data = tabela_clientes_mais_compraram[tabela_clientes_mais_compraram['NOMEFORN'].str.contains(search_term, case=False)]

# Exibindo a tabela filtrada
st.write(filtered_data)