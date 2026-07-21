import streamlit as st
import pandas as pd
from services.coingecko import buscar_moedas, buscar_historico_moeda, buscar_dados_mercado, buscar_mapeamento_moedas
from plots.history_prices import criar_grafico_preco
from processing.history_processing import processar_historico, JANELAS
from processing.market_processing import processar_dados_mercado
from processing.summary_processing import gerar_resumo

st.set_page_config(layout="wide")

st.markdown('## Dashboard de Análise de Criptomoedas')

moedas = buscar_moedas()

ids = moedas['id']
nomes_moedas = buscar_mapeamento_moedas()

col1_select, col2_select = st.columns(2, gap='large')

with col1_select:
    indice_padrao = ids[ids == "bitcoin"].index[0]
    moeda = st.selectbox('Selecione uma CriptoMoeda para ser Analisada', options=ids, format_func=lambda id: nomes_moedas[id], index=indice_padrao)

with col2_select:
    periodo = st.segmented_control('Período (Dias)', JANELAS, default=30)

historico_moeda = buscar_historico_moeda(moeda, periodo)
historico_moeda = processar_historico(historico_moeda)
dados_mercado = buscar_dados_mercado(moeda)
dados_mercado = processar_dados_mercado(dados_mercado, historico_moeda)
resumo_moedas = gerar_resumo(historico_moeda, dados_mercado)

preco_col, variacao_col, market_cap_col, ranking_col = st.columns(4)

with preco_col:
    st.metric("Preço Atual", resumo_moedas["price_fmt"], resumo_moedas["price_diff_fmt"])

with variacao_col:
    st.metric("Retorno Diário", resumo_moedas["daily_return_fmt"])

with market_cap_col:
    st.metric("Market Cap", resumo_moedas["market_cap_fmt"], resumo_moedas["market_cap_change_percentage_24h_fmt"])

with ranking_col:
    st.metric("Posição no Ranking", resumo_moedas["rank_fmt"])

ath_col, distancia_ma_col, volume_col, drawdown_col = st.columns(4, gap="medium")

with ath_col:
    st.metric("ATH (All Time High)", resumo_moedas["ath_fmt"])

with distancia_ma_col:
    st.metric(f"Distância do MA {periodo}", resumo_moedas[f"ma_distance_{periodo}_fmt"])

with volume_col:
    st.metric("Volume", resumo_moedas["volume_fmt"], resumo_moedas[f'volume_delta_{periodo}_fmt'])

with drawdown_col:
    st.metric("Drawdown", resumo_moedas["drawdown_fmt"], resumo_moedas['drawdown_delta_fmt'])
    
grafico_historico = criar_grafico_preco(historico_moeda, periodo)

st.plotly_chart(grafico_historico, use_container_width=True)