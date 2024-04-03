import pandas as pd
import streamlit as st
import streamlit_shadcn_ui as ui

st.set_page_config(layout="wide")

# Carregar os dados
venda_itens = pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/venda_itens.csv', delimiter=';', encoding='latin1')
vendas=pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/venda.csv', delimiter=';', encoding='latin-1')
produtos = pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/produto.csv', delimiter=';', encoding='latin-1')

# Unir os dataframes
vendas_relacao_produtos = pd.merge(produtos[['PCOD','PDESC','PVLUVEN3','PVLUVENDA']],venda_itens[['PCOD','QTDVENDA','VLVENDA']],right_on='PCOD',left_on='PCOD')
vendas_relacao_produtos = vendas_relacao_produtos.groupby(['PCOD','PDESC','PVLUVEN3','PVLUVENDA'])[['QTDVENDA','VLVENDA']].sum().reset_index()
vendas_relacao_produtos = vendas_relacao_produtos.sort_values(by='VLVENDA',ascending=False)
vendas_relacao_produtos['CUSTOCMV'] = vendas_relacao_produtos['PVLUVEN3'] * vendas_relacao_produtos['QTDVENDA']
vendas_relacao_produtos['MARGEM'] = vendas_relacao_produtos['VLVENDA'] - vendas_relacao_produtos['CUSTOCMV']
vendas_relacao_produtos['LUCRO'] = ((vendas_relacao_produtos['MARGEM']) / (vendas_relacao_produtos['VLVENDA'])) * 100
vendas_relacao_produtos['MARKUP'] = (((vendas_relacao_produtos['VLVENDA']) / (vendas_relacao_produtos['CUSTOCMV'])) * 100) -100
vendas_relacao_produtos = vendas_relacao_produtos[['PCOD','PDESC','QTDVENDA','VLVENDA','CUSTOCMV','MARGEM','LUCRO','MARKUP']]

# Construção das variaveis
soma_quantidade = vendas_relacao_produtos['QTDVENDA'].sum()
soma_valor_venda = vendas_relacao_produtos['VLVENDA'].sum() # R$
soma_custo_cmv = vendas_relacao_produtos['CUSTOCMV'].sum() # R$
soma_margem = vendas_relacao_produtos['MARGEM'].sum() # R$
percentual_lucro_final = (soma_margem / soma_valor_venda) * 100
percentual_markup_final = ((soma_valor_venda / soma_custo_cmv) * 100) - 100

# Definir as opções de ordenação
options = {
    "PDESC": "Descrição (Alfabético)",
    "QTDVENDA": "Quantidade Vendida (Decrescente)",
    "VLVENDA": "Valor de Venda (Decrescente)",
    "CUSTOCMV": "Custo CMV (Decrescente)",
    "MARGEM": "Margem (Decrescente)",
    "LUCRO": "Lucro (Decrescente)",
    "MARKUP": "Markup (Decrescente)"
}

# Sidebar
selected_option = st.sidebar.selectbox("Ordenar por:", list(options.values()))

# Pesquisa por código ou nome do produto
search_term = st.text_input("Digite o nome ou código do produto:")

# Filtrar os dados de acordo com o termo de pesquisa
if search_term.isdigit():
    # Pesquisa pelo código do produto
    filtered_data = vendas_relacao_produtos[vendas_relacao_produtos['PCOD'] == int(search_term)]
else:
    # Pesquisa pelo nome do produto
    filtered_data = vendas_relacao_produtos[vendas_relacao_produtos['PDESC'].str.contains(search_term, case=False)]
# Exibir as métricas
if search_term == "":
    quantidade = soma_quantidade
    valor_venda = f'R${soma_valor_venda:,.2f}'
    custo_cmv = f'R${soma_custo_cmv:,.2f}'
    margem = f'R${soma_margem:,.2f}'
else:
    quantidade = filtered_data['QTDVENDA'].sum()
    valor_venda = filtered_data['VLVENDA'].sum()
    custo_cmv = filtered_data['CUSTOCMV'].sum()
    margem = filtered_data['MARGEM'].sum()

    valor_venda = float(valor_venda)
    margem = float(margem)
    custo_cmv = float(custo_cmv)

    percentual_lucro_final = (margem / valor_venda) * 100
    percentual_markup_final = ((valor_venda / custo_cmv) * 100) - 100

    percentual_lucro_final = (margem / valor_venda) * 100
    percentual_markup_final = ((valor_venda / custo_cmv) * 100) - 100


    # Formatando os valores para reais
    valor_venda = f'R${valor_venda:,.2f}'
    margem = f'R${margem:,.2f}'
    custo_cmv = f'R${custo_cmv:,.2f}'

percentual_lucro_final = f'{percentual_lucro_final:.2f}%'
percentual_markup_final = f'{percentual_markup_final:.2f}%'

# Ordenar os dados de acordo com a opção selecionada na sidebar
if selected_option == "Descrição (Alfabético)":
    filtered_data = filtered_data.sort_values(by='PDESC')
elif selected_option == "Quantidade Vendida (Decrescente)":
    filtered_data = filtered_data.sort_values(by='QTDVENDA', ascending=False)
elif selected_option == "Valor de Venda (Decrescente)":
    filtered_data = filtered_data.sort_values(by='VLVENDA', ascending=False)
elif selected_option == "Custo CMV (Decrescente)":
    filtered_data = filtered_data.sort_values(by='CUSTOCMV', ascending=False)
elif selected_option == "Margem (Decrescente)":
    filtered_data = filtered_data.sort_values(by='MARGEM', ascending=False)
elif selected_option == "Lucro (Decrescente)":
    filtered_data = filtered_data.sort_values(by='LUCRO', ascending=False)
elif selected_option == "Markup (Decrescente)":
    filtered_data = filtered_data.sort_values(by='MARKUP', ascending=False)

# Formatação dos dados
filtered_data['PCOD'] = filtered_data['PCOD'].map(str)
filtered_data['VLVENDA'] = filtered_data['VLVENDA'].map(lambda x: f'R$ {x:,.2f}')
filtered_data['CUSTOCMV'] = filtered_data['CUSTOCMV'].map(lambda x: f'R$ {x:,.2f}')
filtered_data['MARGEM'] = filtered_data['MARGEM'].map(lambda x: f'R$ {x:,.2f}')
filtered_data['LUCRO'] = filtered_data['LUCRO'].map(lambda x: f'{x:,.2f}%')
filtered_data['MARKUP'] = filtered_data['MARKUP'].map(lambda x: f'{x:,.2f}%')


# Renomear as colunas
filtered_data_r = filtered_data.rename(columns={'PCOD': 'CODIGO','PDESC':'DESCRIÇÃO', 'QTDVENDA': 'QUANTIDADE','VLVENDA':'VENDA'})

# Exibir os dados filtrados
st.write(filtered_data_r)

cols = st.columns(4)
with cols[0]:
    ui.metric_card(title="QUANTIDADE", content=f'{quantidade}', description="SOMA DAS QUANTIDADES VENDIDAS", key="card1")
with cols[1]:
    ui.metric_card(title="VENDAS", content=f'{valor_venda}', description="SOMA DO VALOR DE VENDA DE CADA PRODUTO", key="card2")
with cols[2]:
    ui.metric_card(title="CUSTO CMV", content=f'{custo_cmv}', description="SOMA DO VALOR DE COMPRA", key="card3")
with cols[3]:
    ui.metric_card(title="MARGEM", content=f'{margem}', description="SOMA DAS MARGENS INDIVIDUAIS DE CADA PRODUTO", key="card4")

cols = st.columns(2)
with cols[0]:
    ui.metric_card(title="LUCRO MÉDIO", content=f'{percentual_lucro_final}', description="PERCENTUAL DO LUCRO BRUTO", key="card5")
with cols[1]:
    ui.metric_card(title="MARKUP MÉDIO", content=f'{percentual_markup_final}', description="PERCENTUAL DO MARKUP MÉDIO", key="card6")