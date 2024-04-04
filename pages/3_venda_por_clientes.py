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

def render_tela_principal():

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
    tabela_clientes_mais_compraram['FVALVENDA'] = tabela_clientes_mais_compraram['FVALVENDA'].map(lambda x: f'R$ {x:,.2f}')
    cols = st.columns(3)
    with cols[0]:
        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig)
    with cols[2]:
        tabela_clientes_mais_compraram = tabela_clientes_mais_compraram.rename(columns={'IDCLI': 'CODIGO','NOMEFORN':'CLIENTE', 'FVALVENDA': 'VALOR COMPRA'})
        st.write(tabela_clientes_mais_compraram)
    # --------------------- PESQUISA DO NOME DO FORNECEDOR --------------------------
    # Remover o símbolo de 'R$' e as vírgulas da coluna FVALVENDA antes de convertê-la para float
    tabela_clientes_mais_compraram['VALOR COMPRA'] = tabela_clientes_mais_compraram['VALOR COMPRA'].map(lambda x: float(x.replace('R$', '').replace(',', '')) if isinstance(x, str) else x)

    # Formatar IDCLI para número inteiro sem vírgulas
    tabela_clientes_mais_compraram['CODIGO'] = tabela_clientes_mais_compraram['CODIGO'].astype(int)

    # PESQUISA DO NOME DO CLIENTE
    search_term = st.text_input("Digite o nome ou código do cliente:")

    # Verificando se o termo de pesquisa é um número (código do cliente)
    if search_term.isdigit():
        # Pesquisa pelo código do cliente
        filtered_data = tabela_clientes_mais_compraram[tabela_clientes_mais_compraram['CODIGO'] == int(search_term)]
    else:
        # Pesquisa pelo nome do cliente
        filtered_data = tabela_clientes_mais_compraram[tabela_clientes_mais_compraram['CLIENTE'].str.contains(search_term, case=False)]

    # Calculando a soma das compras do cliente filtrado
    soma_compras_cliente = filtered_data['VALOR COMPRA'].sum()

    # Exibindo a soma das compras do cliente filtrado
    ui.metric_card(title="VALOR COMPRA", content=f"R$ {soma_compras_cliente:,.2f}", description=f"cliente ou codigo cadastrado: {search_term}")
def render_cliente_sem_compras():
    st.write(clientes)
def render_cliente_em_queda():
    st.write(clientes)

def render_cliente_novos():
    st.write(clientes)

def render_cliente_ascendentes():
    st.write(clientes)

pagina_selecionada = st.sidebar.radio('Selecione a página', ['VENDA POR CLIENTE', 'CLIENTES SEM COMPRA','CLIENTES EM QUEDA','CLIENTES NOVOS','CLIENTES ASCENDENTES'])

# Renderização da página selecionada
if pagina_selecionada == 'VENDA POR CLIENTE':
    render_tela_principal()
elif pagina_selecionada == 'CLIENTES SEM COMPRA':
    render_cliente_sem_compras()
elif pagina_selecionada == 'CLIENTES EM QUEDA':
    render_cliente_em_queda()
elif pagina_selecionada == 'CLIENTES NOVOS':
    render_cliente_novos()
elif pagina_selecionada == 'CLIENTES ASCENDENTES':
    render_cliente_ascendentes()