import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit_shadcn_ui as ui
import pygwalker as pyg

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
#TELA DE PRODUTOS VENDIDOS

# Criando tabela dos produtos que mais venderam
produto_mais_venda = venda_itens.groupby('PCOD')['VLVENDA'].sum().reset_index()

# Localizando os produtos que mais venderam
produto_mais_venda = produto_mais_venda.sort_values(by='VLVENDA', ascending=False)

# Selecionando os top 5 produtos que mais venderam
top_produtos_mais_vendidos = produto_mais_venda.head(5)
# Agora mesclando para saber o nome dos produtos
verifica_nome_produtos_vendas = top_produtos_mais_vendidos.merge(produtos[['PCOD', 'PDESC', 'PUNIDADE', 'PVLUVENDA' , 'PVLUVEN3']], on='PCOD')

# Criando o gráfico de pizza
fig = px.pie(verifica_nome_produtos_vendas, values='VLVENDA', names='PDESC', title='TOP 5 PRODUTOS MAIS VENDIDOS')
st.plotly_chart(fig)

# Criando a tabela que relacionada ao grafico pizza
data = [
    {"PRODUTO": f"{verifica_nome_produtos_vendas.iloc[0]['PDESC']}", "VALOR VENDA": f"R$ {verifica_nome_produtos_vendas.iloc[0]['VLVENDA']:.2f}", "VALOR UNITARIO": f"{verifica_nome_produtos_vendas.iloc[0]['PVLUVENDA']}"},
    {"PRODUTO": f"{verifica_nome_produtos_vendas.iloc[1]['PDESC']}", "VALOR VENDA": f"R$ {verifica_nome_produtos_vendas.iloc[1]['VLVENDA']:.2f}", "VALOR UNITARIO": f"{verifica_nome_produtos_vendas.iloc[1]['PVLUVENDA']}"},
    {"PRODUTO": f"{verifica_nome_produtos_vendas.iloc[2]['PDESC']}", "VALOR VENDA": f"R$ {verifica_nome_produtos_vendas.iloc[2]['VLVENDA']:.2f}", "VALOR UNITARIO": f"{verifica_nome_produtos_vendas.iloc[2]['PVLUVENDA']}"},
    {"PRODUTO": f"{verifica_nome_produtos_vendas.iloc[3]['PDESC']}", "VALOR VENDA": f"R$ {verifica_nome_produtos_vendas.iloc[3]['VLVENDA']:.2f}", "VALOR UNITARIO": f"{verifica_nome_produtos_vendas.iloc[3]['PVLUVENDA']}"},
    {"PRODUTO": f"{verifica_nome_produtos_vendas.iloc[4]['PDESC']}", "VALOR VENDA": f"R$ {verifica_nome_produtos_vendas.iloc[4]['VLVENDA']:.2f}", "VALOR UNITARIO": f"{verifica_nome_produtos_vendas.iloc[4]['PVLUVENDA']}"}
]

# Criando o DataFrame para a exibição
invoice_df = pd.DataFrame(data)
ui.table(data=invoice_df, maxHeight=300)

# -----------------------------------------------------------------

# Criando a tabela que vai ficar os dados do codigo que teve mais unidades vendidas
produto_mais_venda_qtd = venda_itens.groupby('PCOD')['QTDVENDA'].sum().reset_index()

# Localizando os produtos que mais sairam em quantidade
produto_mais_venda_qtd = produto_mais_venda_qtd.sort_values(by='QTDVENDA', ascending=False)

# Selecionando os top 5 produtos que mais venderam
top_produtos_mais_vendidos_qtd = produto_mais_venda_qtd.head(5)

# Agora mesclando para saber o nome dos produtos
verifica_nome_produtos_vendas_qtd = top_produtos_mais_vendidos_qtd.merge(produtos[['PCOD', 'PDESC', 'PUNIDADE', 'PVLUVENDA' , 'PVLUVEN3']], on='PCOD')

# Criando o gráfico de pizza
fig_qtd = px.pie(verifica_nome_produtos_vendas_qtd, values='QTDVENDA', names='PDESC', title='TOP 5 PRODUTOS QUE MAIS FORAM VENDIDOS')
# Exibindo o gráfico de pizza
st.plotly_chart(fig_qtd)

# Criando a tabela que relacionada ao grafico pizza
data_qtd = [
    {"PRODUTO": f"{verifica_nome_produtos_vendas_qtd.iloc[0]['PDESC']}", "QUANTIDADE VENDIDA": f"{verifica_nome_produtos_vendas_qtd.iloc[0]['QTDVENDA']:.2f}", "VALOR UNITARIO": f"{verifica_nome_produtos_vendas_qtd.iloc[0]['PVLUVENDA']}"},
    {"PRODUTO": f"{verifica_nome_produtos_vendas_qtd.iloc[1]['PDESC']}", "QUANTIDADE VENDIDA": f"{verifica_nome_produtos_vendas_qtd.iloc[1]['QTDVENDA']:.2f}", "VALOR UNITARIO": f"{verifica_nome_produtos_vendas_qtd.iloc[1]['PVLUVENDA']}"},
    {"PRODUTO": f"{verifica_nome_produtos_vendas_qtd.iloc[2]['PDESC']}", "QUANTIDADE VENDIDA": f"{verifica_nome_produtos_vendas_qtd.iloc[2]['QTDVENDA']:.2f}", "VALOR UNITARIO": f"{verifica_nome_produtos_vendas_qtd.iloc[2]['PVLUVENDA']}"},
    {"PRODUTO": f"{verifica_nome_produtos_vendas_qtd.iloc[3]['PDESC']}", "QUANTIDADE VENDIDA": f"{verifica_nome_produtos_vendas_qtd.iloc[3]['QTDVENDA']:.2f}", "VALOR UNITARIO": f"{verifica_nome_produtos_vendas_qtd.iloc[3]['PVLUVENDA']}"},
    {"PRODUTO": f"{verifica_nome_produtos_vendas_qtd.iloc[4]['PDESC']}", "QUANTIDADE VENDIDA": f"{verifica_nome_produtos_vendas_qtd.iloc[4]['QTDVENDA']:.2f}", "VALOR UNITARIO": f"{verifica_nome_produtos_vendas_qtd.iloc[4]['PVLUVENDA']}"}
]
# Criando o DataFrame para a exibição
tabela_mais_qtd_venda = pd.DataFrame(data_qtd)
ui.table(data=tabela_mais_qtd_venda, maxHeight=300)
