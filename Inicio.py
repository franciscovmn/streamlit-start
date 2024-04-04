import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit_shadcn_ui as ui
st.set_page_config(layout="wide")
# Carregando os dados
compras = pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/compra.csv', sep=';', encoding='latin1')
vendas = pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/venda.csv', delimiter=';', encoding='latin-1')
fornecedores = pd.read_csv('/Users/FVMN/Documents/GitHub/upciga_streamlit/csv/fornecedores.csv', sep=';', encoding='latin1')

# Calcular a soma das vendas por dia
vendas_dia = vendas.groupby('FDATAEMI')['FVALVENDA'].sum().reset_index()

# Calcular a soma das compras por dia
compras_dia = compras.groupby('FDATAEMI')['FVALCOMPRA'].sum().reset_index()

# Verificar o fornecedor que comprou no dia
compra_fornecedor_dia = pd.merge(compras[['IDFORN','FDATAEMI','FVALCOMPRA']],fornecedores[['IDFORN','NOMEFORN','UF']],how='left',left_on='IDFORN',right_on='IDFORN')
compra_fornecedor_dia = compra_fornecedor_dia.sort_values(by='FDATAEMI', ascending=True)

# Calcular a soma total de vendas e compras
soma_vendas_total = vendas['FVALVENDA'].sum()
soma_compras_total = compras['FVALCOMPRA'].sum()

# Formatar as somas como moeda
soma_vendas_total_str = f'R$ {soma_vendas_total:,.2f}'
soma_compras_total_str = f'R$ {soma_compras_total:,.2f}'

lucro_bruto = soma_vendas_total - soma_compras_total
lucro_bruto_str = f"R$ {lucro_bruto:,.2f}"
cols = st.columns(2)
with cols[0]:
    ui.metric_card(title="COMPRA TOTAL", content=soma_compras_total_str,key="card1")
with cols[1]:
    ui.metric_card(title="VENDA TOTAL", content=soma_vendas_total_str, key="card2")
ui.metric_card(title="LUCRO BRUTO", content=lucro_bruto_str, key="card3")

# ----------------------
# Colocando em ordem
vendas_dia = vendas_dia.sort_values(by='FDATAEMI',ascending=False)
# Converter a coluna 'FDATAEMI' para o formato de data
vendas_dia['FDATAEMI'] = pd.to_datetime(vendas_dia['FDATAEMI'], format='%m/%d/%Y')
# Formatar a data como 'dia/mês/ano'
vendas_dia['FDATAEMI'] = vendas_dia['FDATAEMI'].dt.strftime('%d/%m/%Y')

# Criar uma nova coluna com a soma das vendas formatada como moeda real
vendas_dia['Soma_Vendas_Formatada'] = vendas_dia['FVALVENDA'].map(lambda x: f'R$ {x:,.2f}')

# Plotar o gráfico de linhas horizontais
fig = px.bar(vendas_dia, y='FDATAEMI', x='FVALVENDA', text='Soma_Vendas_Formatada', color='FVALVENDA',
             labels={'FVALVENDA': 'Soma das Vendas'}, orientation='h')

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Soma das Vendas por Dia',
                  xaxis_title='Soma das Vendas',
                  yaxis_title='Data')

# Exibir o gráfico
st.plotly_chart(fig)
# ----------------------

vendas = vendas.reindex(columns=['FDATAEMI','FVALVENDA','HORA','FLOJA'])
# Date Range Picker
dt1 = ui.date_picker(key="date_picker2", mode="range", label="Selecione um intervalo de datas")

# Converter as datas para o formato esperado (mes/dia/ano)
vendas['FDATAEMI'] = pd.to_datetime(vendas['FDATAEMI'], format='%m/%d/%Y')
compra_fornecedor_dia['FDATAEMI'] = pd.to_datetime(compra_fornecedor_dia['FDATAEMI'], format='%m/%d/%Y')

# Aplicar filtro de datas, se selecionado
if dt1 is not None:
    start_date = dt1[0]
    end_date = dt1[1]
    
    # Filtrar o DataFrame com base no intervalo de datas selecionado
    soma_vendas_total_filtradas = vendas[(vendas['FDATAEMI'] >= start_date) & (vendas['FDATAEMI'] <= end_date)]
    compras_filtradas = compra_fornecedor_dia[(compra_fornecedor_dia['FDATAEMI'] >= start_date) & (compra_fornecedor_dia['FDATAEMI'] <= end_date)]

    # Calcular a soma do valor de compra para o período selecionado
    soma_fvalvenda = soma_vendas_total_filtradas['FVALVENDA'].sum()
    soma_fvalcompra = compras_filtradas['FVALCOMPRA'].sum()
    
    # Exibir os dados filtrados
    st.write("Dados filtrados:")
    
    # Criar uma nova coluna com a data formatada para exibição na tabela
    soma_vendas_total_filtradas['FDATAEMI_FORMATADA'] = soma_vendas_total_filtradas['FDATAEMI'].dt.strftime('%d/%m/%Y')
    compras_filtradas['FDATAEMI_FORMATADA'] = compras_filtradas['FDATAEMI'].dt.strftime('%d/%m/%Y')

    soma_vendas_total_filtradas['FVALVENDA'] = soma_vendas_total_filtradas['FVALVENDA'].map(lambda x: f'R$ {x:,.2f}') # Formatar FVALCOMPRA para moeda (Real)
    compras_filtradas['FVALCOMPRA'] = compras_filtradas['FVALCOMPRA'].map(lambda x: f'R$ {x:,.2f}') # Formatar FVALCOMPRA para moeda (Real)
    compras_filtradas['IDFORN'] = compras_filtradas['IDFORN'].map(lambda x: f'{x:}')

    compras_filtradas=compras_filtradas[['FVALCOMPRA','FDATAEMI_FORMATADA','NOMEFORN','UF','IDFORN','FDATAEMI']]
    # Exibir a soma do valor de compra em um card
    cols_c = st.columns(2)
    with cols_c[0]:
        ui.metric_card(title="Total Vendas", content=f"R$ {soma_fvalvenda:,.2f}", description="SOMA TOTAL ATÉ O DIA ATUAL")
    with cols_c[1]:
        ui.metric_card(title="Total Compras", content=f"R$ {soma_fvalcompra:,.2f}", description="SOMA TOTAL ATÉ O DIA ATUAL")

    soma_vendas_total_filtradas = soma_vendas_total_filtradas.rename(columns={'FVALVENDA': 'VALOR DA VENDA', 'FLOJA': 'LOJA','FDATAEMI_FORMATADA':'DATA DA VENDA'})
    compras_filtradas = compras_filtradas.rename(columns={'FVALCOMPRA': 'VALOR DA COMPRA', 'NOMEFORN': 'CLIENTE','FDATAEMI_FORMATADA':'DATA DA COMPRA','IDFORN':'CODIGO DO CLIENTE'})
    compras_filtradas['CLIENTE'] = compras_filtradas['CLIENTE'].fillna('Consumidor Final')
    compras_filtradas['UF'] = compras_filtradas['UF'].fillna('PB')

    cols = st.columns(2)
    with cols[0]:
        st.write(soma_vendas_total_filtradas.drop(columns=['FDATAEMI']))  # Exclua a coluna original
    with cols[1]:
        st.write(compras_filtradas.drop(columns=['FDATAEMI']))  # Exclua a coluna original
        
else:
    st.write("Nenhum intervalo de datas selecionado.")
