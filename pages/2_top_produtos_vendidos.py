import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit_shadcn_ui as ui
import pygwalker as pyg

st.set_page_config(layout="wide")

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

# Criando tabela dos produtos que mais venderam
produto_mais_venda = venda_itens.groupby('PCOD')[['VLVENDA','QTDVENDA']].sum().reset_index()

# Localizando os produtos que mais venderam
produto_mais_venda = produto_mais_venda.sort_values(by='VLVENDA', ascending=False)

# Selecionando os top 5 produtos que mais venderam
top_produtos_mais_vendidos = produto_mais_venda.head(5)
# Agora mesclando para saber o nome dos produtos
verifica_nome_produtos_vendas = top_produtos_mais_vendidos.merge(produtos[['PCOD', 'PDESC', 'PUNIDADE', 'PVLUVENDA' , 'PVLUVEN3']], on='PCOD')

# Criando o gráfico de pizza valor venda
fig = px.pie(verifica_nome_produtos_vendas, values='VLVENDA', names='PDESC', title='TOP 5 PRODUTOS MAIS VENDIDOS')

# -----------------------------------------------------------------

# Criando a tabela que vai ficar os dados do codigo que teve mais unidades vendidas
produto_mais_venda_qtd = venda_itens.groupby('PCOD')[['QTDVENDA','VLVENDA']].sum().reset_index()

# Localizando os produtos que mais sairam em quantidade
produto_mais_venda_qtd = produto_mais_venda_qtd.sort_values(by='QTDVENDA', ascending=False)

# Selecionando os top 5 produtos que mais venderam
top_produtos_mais_vendidos_qtd = produto_mais_venda_qtd.head(5)

# Agora mesclando para saber o nome dos produtos
verifica_nome_produtos_vendas_qtd = top_produtos_mais_vendidos_qtd.merge(produtos[['PCOD', 'PDESC', 'PUNIDADE', 'PVLUVENDA' , 'PVLUVEN3']], on='PCOD')

# Criando o gráfico de pizza qtd
fig_qtd = px.pie(verifica_nome_produtos_vendas_qtd, values='QTDVENDA', names='PDESC', title='TOP 5 PRODUTOS QUE MAIS FORAM VENDIDOS')

# Adicionando o selectbox para o usuário escolher entre top 5, 10 ou 20
selected_option = st.selectbox("Selecione a quantidade de produtos mais vendidos:",
                                ["Top 5", "Top 10", "Top 20"])

# Determinando o número de produtos a serem exibidos com base na seleção do usuário
if selected_option == "Top 5":
    top_produtos = 5
elif selected_option == "Top 10":
    top_produtos = 10
else:
    top_produtos = 20

# Redefinindo as variáveis com base na escolha do usuário
top_produtos_mais_vendidos = produto_mais_venda.head(top_produtos)
top_produtos_mais_vendidos_qtd = produto_mais_venda_qtd.head(top_produtos)

# Atualizando os gráficos com as novas informações
verifica_nome_produtos_vendas = top_produtos_mais_vendidos.merge(produtos[['PCOD', 'PDESC', 'PUNIDADE', 'PVLUVENDA' , 'PVLUVEN3']], on='PCOD')
verifica_nome_produtos_vendas_qtd = top_produtos_mais_vendidos_qtd.merge(produtos[['PCOD', 'PDESC', 'PUNIDADE', 'PVLUVENDA' , 'PVLUVEN3']], on='PCOD')

if selected_option == "Top 5":
    fig = px.pie(verifica_nome_produtos_vendas, values='VLVENDA', names='PDESC', title=f'TOP {top_produtos} PRODUTOS EM VALOR DE VENDA')
    fig_qtd = px.pie(verifica_nome_produtos_vendas_qtd, values='QTDVENDA', names='PDESC', title=f'TOP {top_produtos} PRODUTOS EM QUANTIDADES')
else:
    fig = px.bar(verifica_nome_produtos_vendas, y='PDESC', x='VLVENDA', orientation='h', title=f'TOP {top_produtos} PRODUTOS EM VALOR DE VENDA')
    fig_qtd = px.bar(verifica_nome_produtos_vendas_qtd, y='PDESC', x='QTDVENDA', orientation='h', title=f'TOP {top_produtos} PRODUTOS EM QUANTIDADES')

cols = st.columns(4)

with cols[0]:
    st.plotly_chart(fig)
    
with cols[2]:
    st.plotly_chart(fig_qtd)

cols_t = st.columns(2)


# Resetar o índice de verifica_nome_produtos_vendas
verifica_nome_produtos_vendas.reset_index(drop=True, inplace=True)

# Formatar PCOD para números inteiros
verifica_nome_produtos_vendas['PCOD'] = verifica_nome_produtos_vendas['PCOD'].map(str)
verifica_nome_produtos_vendas_qtd['PCOD'] = verifica_nome_produtos_vendas_qtd['PCOD'].map(str)

# Formatar 'VLVENDA' para moeda brasileira real
verifica_nome_produtos_vendas['VLVENDA'] = verifica_nome_produtos_vendas['VLVENDA'].map(lambda x: f'R${x:,.2f}')
verifica_nome_produtos_vendas['PVLUVENDA'] = verifica_nome_produtos_vendas['PVLUVENDA'].map(lambda x: f'R${x:,.2f}')

# Selecione as colunas relevantes para verifica_nome_produtos_vendas_qtd
verifica_nome_produtos_vendas_qtd = verifica_nome_produtos_vendas_qtd[['PCOD', 'PDESC', 'QTDVENDA','VLVENDA']]
verifica_nome_produtos_vendas= verifica_nome_produtos_vendas[['PCOD', 'PDESC', 'VLVENDA','QTDVENDA']]

# Formatar 'QTDVENDA' para moeda brasileira real
verifica_nome_produtos_vendas_qtd['QTDVENDA'] = verifica_nome_produtos_vendas_qtd['QTDVENDA'].map(lambda x: f'{x:,.0f}')
verifica_nome_produtos_vendas['QTDVENDA'] = verifica_nome_produtos_vendas['QTDVENDA'].map(lambda x: f'{x:,.0f}')
verifica_nome_produtos_vendas_qtd['VLVENDA'] = verifica_nome_produtos_vendas_qtd['VLVENDA'].map(lambda x: f'R${x:,.2f}')

verifica_nome_produtos_vendas = verifica_nome_produtos_vendas.rename(columns={'PCOD': 'CODIGO', 'PDESC': 'NOME','VLVENDA':'SOMA VENDAS','QTDVENDA':'QUANTIDADE VENDIDA'})
verifica_nome_produtos_vendas_qtd = verifica_nome_produtos_vendas_qtd.rename(columns={'PCOD': 'CODIGO', 'PDESC': 'NOME','VLVENDA':'SOMA VENDAS','QTDVENDA':'QUANTIDADE VENDIDA'})

# Mostrar a tabela embaixo do respectivo gráfico
with cols_t[0]:
    st.write(verifica_nome_produtos_vendas)
with cols_t[1]:
    st.write(verifica_nome_produtos_vendas_qtd)
