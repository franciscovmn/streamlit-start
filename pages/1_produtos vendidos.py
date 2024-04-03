import pandas as pd
import streamlit as st
import streamlit_shadcn_ui as ui
import plotly.express as px

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

def render_pagina_principal():
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

def render_pagina_consulta_periodo():
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
def produto_sc():
    st.write(verifica_nome_produtos_vendas)
def produto_qd():
    st.write(verifica_nome_produtos_vendas)
def produto_nv():
    st.write(verifica_nome_produtos_vendas)
def produto_as():
    st.write(verifica_nome_produtos_vendas)
pagina_selecionada = st.sidebar.radio('Selecione a página', ['PRODUTOS VENDIDOS', 'TOP PRODUTOS VENDIDOS','PRODUTOS NAO VENDIDOS','PRODUTOS EM QUEDA','PRODUTOS NOVOS','PRODUTOS ASCENDENTES'])

# Renderização da página selecionada
if pagina_selecionada == 'PRODUTOS VENDIDOS':
    render_pagina_principal()
elif pagina_selecionada == 'TOP PRODUTOS VENDIDOS':
    render_pagina_consulta_periodo()
elif pagina_selecionada == 'PRODUTOS NAO VENDIDOS':
    produto_sc()
elif pagina_selecionada == 'PRODUTOS EM QUEDA':
    produto_qd()
elif pagina_selecionada == 'PRODUTOS NOVOS':
    produto_nv()
elif pagina_selecionada == 'PRODUTOS ASCENDENTES':
    produto_as()