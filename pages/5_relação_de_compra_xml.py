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

# Função para renderizar a página principal
def render_pagina_principal():
    # Localizando o fornecedor que eu mais comprei
    fornecedor_mais_compra = compras.groupby('IDFORN')['FVALCOMPRA'].sum().reset_index()

    fornecedor_mais_compra = fornecedor_mais_compra.sort_values(by='FVALCOMPRA', ascending=False)

    nome_fornecedor_mais_compra = fornecedor_mais_compra.merge(fornecedores,on='IDFORN')

    # Visualizando as datas de compra
    data_compra_fornecedor = compras.groupby('FDATAEMI')['FVALCOMPRA'].sum().reset_index()

    data_compra_fornecedor = data_compra_fornecedor.sort_values(by='FDATAEMI',ascending=True)

    data_compra_fornecedor['FDATAEMI'] = pd.to_datetime(data_compra_fornecedor['FDATAEMI'], format='%m/%d/%Y')
    data_compra_fornecedor['FDATAEMI'] = data_compra_fornecedor['FDATAEMI'].dt.strftime('%d/%m/%Y') # Convertendo para a data dia/mes/ano

    # Calcular a soma da coluna 'FVALCOMPRA' e converter para float
    soma_compra_xml = compras['FVALCOMPRA'].sum()

    # Formatar a soma como uma string de moeda (Real)
    soma_compra_xml = f'R$ {soma_compra_xml:,.2f}'

    # Organizando as colunas
    nome_fornecedor_mais_compra['FVALCOMPRA'] = nome_fornecedor_mais_compra['FVALCOMPRA'].map(lambda x: f'R$ {x:,.2f}') # Formatar FVALCOMPRA para moeda (Real)
    nome_fornecedor_mais_compra = nome_fornecedor_mais_compra.reindex(columns=['IDFORN','NOMEFORN','FVALCOMPRA','UF','CP_CIDADE'])

    # ----------------------------------------------------


    # Pesquisa por código ou nome do produto
    search_term = st.text_input("Digite o nome ou código do produto:")

    # Filtrar os dados de acordo com o termo de pesquisa
    if search_term.isdigit():
        # Pesquisa pelo código do produto
        filtered_data = nome_fornecedor_mais_compra[nome_fornecedor_mais_compra['IDFORN'] == int(search_term)]
    else:
        # Pesquisa pelo nome do produto
        filtered_data = nome_fornecedor_mais_compra[nome_fornecedor_mais_compra['NOMEFORN'].str.contains(search_term, case=False)]
    st.write(filtered_data)
    nome_fornecedor_mais_compra['IDFORN'] = nome_fornecedor_mais_compra['IDFORN'].apply(lambda x: f'{x:,}'.replace(',', ''))
    if search_term == "":
        ui.metric_card(title="Total Compra", content=soma_compra_xml, description="SOMA TOTAL ATÉ O DIA ATUAL")
    else:
        soma_compra_xml = filtered_data['FVALCOMPRA'].sum()
        ui.metric_card(title="Total Compra", content=soma_compra_xml, description=f"SOMA TOTAL DO CLIENTE {search_term}")

# Função para renderizar a página de consulta por período
def render_pagina_consulta_periodo():
    # Date Range Picker
    dt2 = ui.date_picker(key="date_picker2", mode="range", label="Selecione um intervalo de datas")

    # Converter as datas para o formato esperado (mes/dia/ano)
    compras['FDATAEMI'] = pd.to_datetime(compras['FDATAEMI'], format='%m/%d/%Y')

    # Aplicar filtro de datas, se selecionado
    if dt2 is not None:
        start_date = dt2[0]
        end_date = dt2[1]
        
        # Filtrar o DataFrame com base no intervalo de datas selecionado
        compras_filtradas = compras[(compras['FDATAEMI'] >= start_date) & (compras['FDATAEMI'] <= end_date)]
        
        # Calcular a soma do valor de compra para o período selecionado
        soma_fvalcompra = compras_filtradas['FVALCOMPRA'].sum()
        
        # Exibir os dados filtrados
        st.write("Dados filtrados:")
        
        # Criar uma nova coluna com a data formatada para exibição na tabela
        compras_filtradas['FDATAEMI_formatada'] = compras_filtradas['FDATAEMI'].dt.strftime('%d/%m/%Y')
        
        # Exibir a tabela com a data formatada
        st.write(compras_filtradas.drop(columns=['FDATAEMI']))  # Exclua a coluna original
        
        # Exibir a soma do valor de compra em um card

        ui.metric_card(title="Total Compra", content=f"R$ {soma_fvalcompra:,.2f}", description="SOMA TOTAL ATÉ O DIA ATUAL")
    else:
        st.write("Nenhum intervalo de datas selecionado.")
pagina_selecionada = st.sidebar.radio('Selecione a página', ['CONSULTA FORNECEDORES', 'CONSULTA POR PERIODO'])

# Renderização da página selecionada
if pagina_selecionada == 'CONSULTA FORNECEDORES':
    render_pagina_principal()
elif pagina_selecionada == 'CONSULTA POR PERIODO':
    render_pagina_consulta_periodo()