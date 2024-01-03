import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

# Carrega o DataFrame a partir do arquivo CSV
dataframe = pd.read_csv('dados.csv')

# Converte a coluna 'Data' para o formato datetime
dataframe['Data'] = pd.to_datetime(dataframe['Data'], errors='coerce')

# Cria colunas 'Ano', 'Mes', 'Dia' a partir da coluna 'Data'
dataframe['Ano'] = dataframe['Data'].dt.strftime('%Y')
dataframe['Mes'] = dataframe['Data'].dt.strftime('%m')
dataframe['Dia'] = dataframe['Data'].dt.strftime('%d')

# Formata a coluna 'Data' no estilo 'dia/mês'
dataframe['Data'] = dataframe['Data'].dt.strftime('%d/%m')

# Verifica se há valores nulos na coluna 'Data'
if dataframe['Data'].isnull().any():
    st.warning("Há valores nulos na coluna 'Data'. Alguns recursos podem não funcionar corretamente.")

# Configuração da página do Streamlit
st.set_page_config(
    page_title="estudo",
    page_icon=":bar_chart:",
    layout="wide",
    # initial_sidebar_state='collapsed' -> esse comando permite que ao iniciar o streamlit o menu inicie fechado.
)

# Sidebar para seleção dinâmica, incluindo seleção de data
year = st.sidebar.multiselect(
    key=1,
    label='ANO',
    options=dataframe['Ano'].unique(),
    default=dataframe['Ano'].unique()  # Valores padrão
)
month = st.sidebar.multiselect(
    key=2,
    label='MES',
    options=dataframe['Mes'].unique(),
    default=dataframe['Mes'].unique()  # Valores padrão
)
store = st.sidebar.multiselect(
    key=3,
    label='LOJA',
    options=dataframe['Loja'].unique(),
    default=dataframe['Loja'].unique()  # Valores padrão
)

filtered_df = dataframe.query('Ano.isin(@year) and Mes.isin(@month) and Loja.isin(@store)')

# Header
st.header(":bar_chart: Sales Dashboard")
st.markdown('#')

# Métricas em Cartões Alinhados
col1, col2, col3, col4 = st.columns(4)

# Calcula métricas
total_vendas = round(filtered_df['Venda'].sum(), 2)
quantidade_vendida = round(filtered_df['Quantidade'].sum())
loja_mais_venda = filtered_df['Loja'].value_counts().idxmax()

# Agrupa os dados pelo vendedor e calcula a soma das vendas para cada um
vendas_por_vendedor = dataframe.groupby('Vendedor')['Venda'].sum()

# Encontra o vendedor que teve o maior valor total de vendas
vendedor_mais_vendas = vendas_por_vendedor.idxmax()

# Encontra o valor total de vendas desse vendedor
valor_mais_vendas = vendas_por_vendedor.max()

# Encontra o vendedor que teve o menor valor total de vendas
vendedor_menos_vendas = vendas_por_vendedor.idxmin()

# Encontra o valor total de vendas desse vendedor
valor_menos_vendas = vendas_por_vendedor.min()

# Calcula o ticket médio
ticket_medio = round((total_vendas / quantidade_vendida), 2)

# Cartões na mesma linha
col1.metric('TOTAL DAS VENDAS', f'R${total_vendas}')
col2.metric('LOJA QUE MAIS VENDEU', loja_mais_venda)
col3.metric('TICKET MÉDIO', f'R${ticket_medio}')

# Cartões na linha abaixo
col4.subheader('VENDEDOR QUE MAIS E MENOS VENDEU')
col4.metric(f'Mais Vendeu: {vendedor_mais_vendas}', f'R${valor_mais_vendas}')
col4.metric(f'Menos Vendeu: {vendedor_menos_vendas}', f'R${valor_menos_vendas}')

# Gráfico de Vendas por Loja
st.subheader('GRÁFICO DE VENDAS POR LOJA')
fig = px.bar(filtered_df, x='Mes', y='Venda', color='Loja', title='Vendas por Loja ao Longo do Tempo')
st.plotly_chart(fig)

# Organização do DataFrame
st.subheader('DADOS DETALHADOS')
st.dataframe(filtered_df.style.set_properties(**{'text-align': 'center'}))

# Agrupa os dados por hora e loja, somando as vendas
vendas_por_hora_loja = dataframe.groupby(['Hora', 'Loja'])['Venda'].sum().reset_index()

# Cria o gráfico de barras empilhadas
fig = px.bar(vendas_por_hora_loja, x='Hora', y='Venda', color='Loja',
             title='Vendas por Hora - Loja 1 vs Loja 2',
             labels={'Venda': 'Total de Vendas', 'Hora': 'Hora do Dia'})

# Adiciona um layout mais informativo
fig.update_layout(
    xaxis_title='Hora do Dia',
    yaxis_title='Total de Vendas',
    barmode='stack',  # Barras empilhadas
)

# Mostra o gráfico no Streamlit
st.subheader('ILUSTRAÇÃO DOS RESULTADOS - Horários de Pico')
st.plotly_chart(fig)

#MODELO CRIADO PELO CHATGPT
# Sidebar: Criando filtros
#Year = st.sidebar.multiselect("Ano", dataframe['Ano'].unique(), default=dataframe['Ano'].unique())
#Month = st.sidebar.multiselect("Mês", dataframe['Mes'].unique(), default=dataframe['Mes'].unique())
#Store = st.sidebar.multiselect("Loja", dataframe['Loja'].unique(), default=dataframe['Loja'].unique())
#Client = st.sidebar.multiselect("Clientes", dataframe['Cliente'].unique(), default=dataframe['Cliente'].unique())

# Aplicando os filtros ao dataframe
#filtered_dataframe = dataframe.query('Ano.isin(@Year) and Mes.isin(@Month) and Loja.isin(@Store) and Cliente.isin(@Client)')

# Exibindo o dataframe filtrado
#if not filtered_dataframe.empty:
#    st.dataframe(filtered_dataframe)
#else:
#    st.info("Aplique filtros para visualizar os dados.")

# Resumo em Cards
#st.markdown('''- - -''')

# Calculando resumo
#total_vendas = round(filtered_dataframe['Venda'].sum(), 2) if not filtered_dataframe.empty else 0
#total_quant = round(filtered_dataframe['Quantidade'].sum()) if not filtered_dataframe.empty else 0
#loja_mais_venda = filtered_dataframe['Loja'].value_counts().idxmax() if not filtered_dataframe.empty else "N/A"
#ticket_medio = round((total_vendas / total_quant)) if total_quant > 0 else 0
#cliente_mais_compra = filtered_dataframe['Cliente'].value_counts().idxmax() if not filtered_dataframe.empty else "N/A"


# Organizando as colunas
#columns = st.columns(5)

# Exibindo resumo em Cards
#with columns[0]:
#    st.info(f"**VENDA TOTAL:**\n${total_vendas}")

#with columns[1]:
#    st.info(f"**QUANTIDADE VENDIDA:**\n{total_quant} unidades")

#with columns[2]:
#    st.info(f"**LOJA QUE MAIS VENDEU:**\n{loja_mais_venda}")

#with columns[3]:
#    st.info(f"**TICKET MÉDIO:**\n${ticket_medio}")

#with columns[4]:
#    st.info(f"**CLIENTE QUE MAIS COMPROU:**\n{cliente_mais_compra}")
#""""""
# st.markdown('''
    # titulo markdown ->  titulo principal
    ## subtitulo -> titulo secundario
#    > texto -> põe um | antes do texto(isso se faz com o '>')
    #
#    > *italico* -> um texto entre '*' deixa italico
    #
#    > **negrito** -> o texto com dois '**' deixa em negrito
# ''')l
