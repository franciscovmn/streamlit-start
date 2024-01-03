import pandas as pd
import streamlit as st
import plotly.express as px

# Carregando os dados
compra_itens = pd.read_csv('compra_itens.csv', delimiter=';')
produtos = pd.read_csv('produto.csv', delimiter=';', encoding='latin-1')
# Carregando os dados
compras = pd.read_csv('compra.csv', sep=';', encoding='latin1')
fornecedores = pd.read_csv('fornecedores.csv', sep=';', encoding='latin1')


# Processamento dos dados
total_vendas = compra_itens.groupby('PCOD')['VLCOMPRA'].sum().reset_index()
idx_maior_valor = total_vendas['VLCOMPRA'].idxmax()
idx_menor_valor = total_vendas['VLCOMPRA'].idxmin()

produto_maior_valor = total_vendas.loc[[idx_maior_valor]]
produto_menor_valor = total_vendas.loc[[idx_menor_valor]]

# Encontrando os nomes dos produtos
produto_maior_valor = produto_maior_valor.merge(produtos, on='PCOD')
produto_menor_valor = produto_menor_valor.merge(produtos, on='PCOD')

# Salvando nas variáveis
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

produto_maior_qtd = total_vendas[total_vendas['PCOD'] == total_qtd['PCOD'][idx_maior_qtd]]
produto_menor_qtd = total_vendas[total_vendas['PCOD'] == total_qtd['PCOD'][idx_menor_qtd]]

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
compras['FVALCOMPRA'] = pd.to_numeric(compras['FVALCOMPRA'], errors='coerce')

# Agrupando por IDFORN e somando os valores de FVALCOMPRA
total_compras_por_fornecedor = compras.groupby('IDFORN')['FVALCOMPRA'].sum().reset_index()

# Encontrando o ID do fornecedor com maior valor de compras
id_forn_maior_valor = total_compras_por_fornecedor.loc[total_compras_por_fornecedor['FVALCOMPRA'].idxmax()]

# Encontrando o ID do fornecedor com menor valor de compras
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
