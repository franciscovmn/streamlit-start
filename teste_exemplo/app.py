import pandas as pd
import streamlit as st
import plotly.express as px

# Carregando os dados
compra_itens = pd.read_csv('compra_itens.csv', delimiter=';')
produtos = pd.read_csv('produto.csv', delimiter=';', encoding='latin-1')
# Carregando os dados
compras = pd.read_csv('compra.csv', sep=';', encoding='latin1')
fornecedores = pd.read_csv('fornecedores.csv', sep=';', encoding='latin1')
vendas=pd.read_csv('venda.csv', delimiter=';', encoding='latin-1')
clientes=pd.read_csv('clientes.csv', delimiter=';', encoding='latin-1')
# Mesclando as tabelas vendas e clientes
venda_cliente = pd.merge(vendas[['FLOJA','IDPEDIDO','IDCLI','SI_CAIXA','FDATAEMI','HORA','FVALVENDA']],clientes[['IDFORN','NOMEFORN']],how='left',left_on='IDCLI',right_on='IDFORN')
venda_cliente.rename(columns= {'NOMEFORN': 'NOMECLI'},inplace=True)
venda_cliente.drop('IDFORN', axis='columns')
# Substituindo NaN por Consumidor Final
venda_cliente['NOMECLI'].fillna('Consumidor Final', inplace=True)

# Agrupando o codigo com o maior valor de compra ( utilizando o groupby para agrupar e o sum() para somar o VLCOMPRA e o reset_index() para poder apagar os indices e ordenar novamente)
total_vendas = compra_itens.groupby('PCOD')['VLCOMPRA'].sum().reset_index()

# Localizando os indices de maior e menor valor de compra da coluna VLCOMPRA
idx_maior_valor = total_vendas['VLCOMPRA'].idxmax()
idx_menor_valor = total_vendas['VLCOMPRA'].idxmin()

# Esta localizando o indice e oque contem na linha
produto_maior_valor = total_vendas.loc[[idx_maior_valor]]
produto_menor_valor = total_vendas.loc[[idx_menor_valor]]

# Mesclando as tabelas para encontrar o respectivo nome do produto com maior e menor valor de compra
produto_maior_valor = produto_maior_valor.merge(produtos, on='PCOD')
produto_menor_valor = produto_menor_valor.merge(produtos, on='PCOD')

# Salvando nas variáveis como vai aparecer na tela do streamlit
cprodmaiorvalor = f"{produto_maior_valor['PDESC'].iloc[0]} (PCOD: {produto_maior_valor['PCOD'].iloc[0]}) - R$ {produto_maior_valor['VLCOMPRA'].iloc[0]:.2f}"
cprodmenorvalor = f"{produto_menor_valor['PDESC'].iloc[0]} (PCOD: {produto_menor_valor['PCOD'].iloc[0]}) - R$ {produto_menor_valor['VLCOMPRA'].iloc[0]:.2f}"

# Apresentando no Streamlit
st.title("Análise de Vendas")
st.markdown("---")  # Linha separadora

st.subheader("Produto com Maior Valor de Compras")
st.markdown(f"**{cprodmaiorvalor}**")

st.subheader("Produto com Menor Valor de Compras")
st.markdown(f"**{cprodmenorvalor}**")

st.markdown("---")  # Linha separadora

# Agregando a quantidade total de compra por produto
total_qtd = compra_itens.groupby('PCOD')['QTDCOMPRA'].sum().reset_index()

# Encontrando o PCOD com maior e menor quantidade de pedidos
idx_maior_qtd = total_qtd['QTDCOMPRA'].idxmax()
idx_menor_qtd = total_qtd['QTDCOMPRA'].idxmin()

# Esta verificando na coluna PCOD da tabela 'total_vendas' o indice que correspondeu a maior quantidade de compras
produto_maior_qtd = total_vendas.loc[[idx_maior_qtd]]
produto_menor_qtd = total_vendas.loc[[idx_menor_qtd]]

# Encontrando os nomes dos produtos
produto_maior_qtd = produto_maior_qtd.merge(produtos, on='PCOD')
produto_menor_qtd = produto_menor_qtd.merge(produtos, on='PCOD')

# Salvando nas variáveis
cprodmaiorqtd = f"{produto_maior_qtd['PDESC'].iloc[0]} (PCOD: {produto_maior_qtd['PCOD'].iloc[0]}) - Quantidade: {total_qtd['QTDCOMPRA'][idx_maior_qtd]}, Valor Total: R$ {produto_maior_qtd['VLCOMPRA'].iloc[0]:.2f}"
cprodmenorqtd = f"{produto_menor_qtd['PDESC'].iloc[0]} (PCOD: {produto_menor_qtd['PCOD'].iloc[0]}) - Quantidade: {total_qtd['QTDCOMPRA'][idx_menor_qtd]}, Valor Total: R$ {produto_menor_qtd['VLCOMPRA'].iloc[0]:.2f}"

# Apresentando no Streamlit
st.subheader("Produto com Maior Quantidade de Pedidos")
st.markdown(f"**{cprodmaiorqtd}**")

st.subheader("Produto com Menor Quantidade de Pedidos")
st.markdown(f"**{cprodmenorqtd}**")

st.markdown("---")  # Linha separadora

# Convertendo FVALCOMPRA para numérico (caso não esteja)
# O errors='coerce' é para se na conversao existir algum valor vazio, ele preencher com nan ( vazio )
compras['FVALCOMPRA'] = pd.to_numeric(compras['FVALCOMPRA'], errors='coerce')

# Agrupando por IDFORN e somando os valores de FVALCOMPRA
total_compras_por_fornecedor = compras.groupby('IDFORN')['FVALCOMPRA'].sum().reset_index()

# Encontrando o ID do fornecedor com maior e menor valor de compras
id_forn_maior_valor = total_compras_por_fornecedor.loc[total_compras_por_fornecedor['FVALCOMPRA'].idxmax()]
id_forn_menor_valor = total_compras_por_fornecedor.loc[total_compras_por_fornecedor['FVALCOMPRA'].idxmin()]

# Unindo os dados com os detalhes dos fornecedores
detalhes_forn_maior_valor = pd.merge(pd.DataFrame([id_forn_maior_valor]), fornecedores, on='IDFORN', how='left')
detalhes_forn_menor_valor = pd.merge(pd.DataFrame([id_forn_menor_valor]), fornecedores, on='IDFORN', how='left')
# Formatando FVALCOMPRA como moeda (R$)
detalhes_forn_maior_valor['FVALCOMPRA'] = detalhes_forn_maior_valor['FVALCOMPRA'].apply(lambda x: "R$ {:.2f}".format(x))
detalhes_forn_menor_valor['FVALCOMPRA'] = detalhes_forn_menor_valor['FVALCOMPRA'].apply(lambda x: "R$ {:.2f}".format(x))

# Exibindo os resultados com formatação
st.markdown("### Fornecedor com maior valor de compras")
st.markdown("**CODIGO DO FORNECEDOR::** " + str(detalhes_forn_maior_valor['IDFORN'].iloc[0]))
st.markdown("**NOME DO FORNECEDOR:** " + detalhes_forn_maior_valor['NOMEFORN'].iloc[0])
st.markdown("**CIDADE:** " + detalhes_forn_maior_valor['CP_CIDADE'].iloc[0])
st.markdown("**UF:** " + detalhes_forn_maior_valor['UF'].iloc[0])
st.markdown("**SOMA DA COMPRA:** " + str(detalhes_forn_maior_valor['FVALCOMPRA'].iloc[0]))

st.markdown("---")  # Linha separadora

st.markdown("### Fornecedor com menor valor de compras")
st.markdown("**CODIGO DO FORNECEDOR:** " + str(detalhes_forn_menor_valor['IDFORN'].iloc[0]))
st.markdown("**NOME DO FORNECEDOR:** " + detalhes_forn_menor_valor['NOMEFORN'].iloc[0])
st.markdown("**CIDADE:** " + detalhes_forn_menor_valor['CP_CIDADE'].iloc[0])
st.markdown("**UF:** " + detalhes_forn_menor_valor['UF'].iloc[0])
st.markdown("**SOMA DA COMPRA:** " + str(detalhes_forn_menor_valor['FVALCOMPRA'].iloc[0]))

st.markdown("---")  # Linha separadora

# Contando pedidos por fornecedor
contagem_pedidos = compras['IDFORN'].value_counts()

# Identificando o fornecedor com mais e menos pedidos
id_forn_mais_pedidos = contagem_pedidos.idxmax()
id_forn_menos_pedidos = contagem_pedidos.idxmin()

# Encontrando as informações dos fornecedores
info_forn_mais_pedidos = fornecedores[fornecedores['IDFORN'] == id_forn_mais_pedidos]
info_forn_menos_pedidos = fornecedores[fornecedores['IDFORN'] == id_forn_menos_pedidos]
# Identificando a quantidade de recorrências e datas para o fornecedor com mais pedidos

qtd_mais_pedidos = contagem_pedidos[id_forn_mais_pedidos]
datas_mais_pedidos = compras[compras['IDFORN'] == id_forn_mais_pedidos]['FDATAEMI']

# Identificando a quantidade de recorrências e datas para o fornecedor com menos pedidos
qtd_menos_pedidos = contagem_pedidos[id_forn_menos_pedidos]
datas_menos_pedidos = compras[compras['IDFORN'] == id_forn_menos_pedidos]['FDATAEMI']

# Exibindo os resultados com formatação
st.markdown("### Fornecedor com maior recorrencia de compra")
st.markdown("**CODIGO DO FORNECEDOR::** " + str(info_forn_mais_pedidos['IDFORN'].iloc[0]))
st.markdown("**NOME DO FORNECEDOR:** " + info_forn_mais_pedidos['NOMEFORN'].iloc[0])
st.markdown("**CIDADE:** " + info_forn_mais_pedidos['CP_CIDADE'].iloc[0])
st.markdown("**UF:** " + info_forn_mais_pedidos['UF'].iloc[0])
st.markdown("**QUANTIDADE DE COMPRAS:** " + str(qtd_mais_pedidos))
st.markdown("**DATAS DAS COMPRAS:** " + ', '.join(datas_mais_pedidos.astype(str)))


st.markdown("---")  # Linha separadora

st.markdown("### Fornecedor com menor recorrencia de compras")
st.markdown("**CODIGO DO FORNECEDOR:** " + str(info_forn_menos_pedidos['IDFORN'].iloc[0]))
st.markdown("**NOME DO FORNECEDOR:** " + info_forn_menos_pedidos['NOMEFORN'].iloc[0])
st.markdown("**CIDADE:** " + info_forn_menos_pedidos['CP_CIDADE'].iloc[0])
st.markdown("**UF:** " + info_forn_menos_pedidos['UF'].iloc[0])
st.markdown("**QUANTIDADE DE COMPRAS:** " + str(qtd_menos_pedidos))
st.markdown("**DATAS DAS COMPRAS:** " + ', '.join(datas_menos_pedidos.astype(str)))
st.markdown("---")  # Linha separadora

# Corrigindo a formatação da data
venda_cliente['FDATAEMI'] = pd.to_datetime(venda_cliente['FDATAEMI'], format='%m/%d/%Y')

# Removendo os clientes com 'Consumidor Final'
df_filtrado = venda_cliente[venda_cliente['NOMECLI'] != 'Consumidor Final']

# Cliente que mais comprou
cliente_mais_compra = df_filtrado.groupby('IDCLI')['FVALVENDA'].sum().idxmax()
nome_cliente_mais = df_filtrado[df_filtrado['IDCLI'] == cliente_mais_compra]['NOMECLI'].iloc[0]
total_cliente_mais = df_filtrado.groupby('IDCLI')['FVALVENDA'].sum().max()

# Cliente que menos comprou
cliente_menos_compra = df_filtrado.groupby('IDCLI')['FVALVENDA'].sum().idxmin()
nome_cliente_menos = df_filtrado[df_filtrado['IDCLI'] == cliente_menos_compra]['NOMECLI'].iloc[0]
total_cliente_menos = df_filtrado.groupby('IDCLI')['FVALVENDA'].sum().min()

# Cliente mais recorrente em compras
df_filtrado['semana_do_ano'] = venda_cliente['FDATAEMI'].dt.isocalendar().week
cliente_mais_recorrente = df_filtrado.groupby('IDCLI')['semana_do_ano'].value_counts().idxmax()[0]
freq_cliente_mais = df_filtrado.groupby('IDCLI')['semana_do_ano'].value_counts().max()
valor_medio_cliente_mais = df_filtrado[df_filtrado['IDCLI'] == cliente_mais_recorrente]['FVALVENDA'].mean()

# Cliente menos recorrente em compras
cliente_menos_recorrente = df_filtrado.groupby('IDCLI')['semana_do_ano'].value_counts().idxmin()[0]
freq_cliente_menos = df_filtrado.groupby('IDCLI')['semana_do_ano'].value_counts().min()
valor_medio_cliente_menos = df_filtrado[df_filtrado['IDCLI'] == cliente_menos_recorrente]['FVALVENDA'].mean()

# Ticket médio por cliente
ticket_medio = df_filtrado.groupby('IDCLI')['FVALVENDA'].mean()

# Arrecadação mensal
arrecadacao_mensal = venda_cliente['FVALVENDA'].sum()


# Utilizando st.write para exibir as informações em formato de texto
st.write(f"Ticket Médio por Cliente: ${ticket_medio.mean():.2f}")
st.write(f"Arrecadação Mensal: ${arrecadacao_mensal:.2f}")

# Alternativamente, você pode usar st.metric para um visual mais estilo "card"
st.metric(label="Cliente que Mais Comprou", value=f"{nome_cliente_mais} (Código: {cliente_mais_compra})", delta=f"Total Comprado: ${total_cliente_mais:.2f}")
st.metric(label="Cliente que Menos Comprou", value=f"{nome_cliente_menos} (Código: {cliente_menos_compra})", delta=f"Total Comprado: ${total_cliente_menos:.2f}")
