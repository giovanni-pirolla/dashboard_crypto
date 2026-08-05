import streamlit as st

from services.coingecko import (
    buscar_moedas,
    buscar_historico_moeda,
    buscar_dados_mercado,
    buscar_mapeamento_moedas
)

from plots.history_prices import criar_grafico_preco
from processing.history_processing import processar_historico, JANELAS
from processing.market_processing import processar_dados_mercado

from utils.formatting import formatar_numero

st.set_page_config(layout="wide")

st.markdown("## Dashboard de Análise de Criptomoedas")

# 
moedas = buscar_moedas()

ids = moedas["id"]
nomes_moedas = buscar_mapeamento_moedas()

# Colunas dos inputs
col1_select, col2_select = st.columns(2, gap="large")

with col1_select:
    indice_padrao = ids[ids == "bitcoin"].index[0]

    moeda = st.selectbox(
        "Selecione uma CriptoMoeda para ser Analisada",
        options=ids,
        format_func=lambda id: nomes_moedas[id],
        index=indice_padrao
    )

with col2_select:
    periodo = st.segmented_control(
        "Período (Dias)",
        JANELAS,
        default=30
    )

# Carregamento dos dados processados
historico_moeda = buscar_historico_moeda(moeda, periodo)
historico_moeda = processar_historico(historico_moeda)

dados_mercado = buscar_dados_mercado(moeda)
dados_mercado = processar_dados_mercado(dados_mercado, historico_moeda)

ultimo_historico = historico_moeda.iloc[-1]
ultimo_mercado = dados_mercado.iloc[-1]

st.divider()

# Colunas de Métricas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Preço Atual",
        f"${ultimo_historico['price']:,.2f}",
        f"{ultimo_historico['daily_return']:.2f}%"
    )

with col2:
    st.metric(
        "Retorno Diário",
        f"{ultimo_historico['daily_return']:.2f}%"
    )

with col3:
    st.metric(
        "Market Cap",
        formatar_numero(ultimo_mercado["market_cap"]),
        # f"{ultimo_mercado['market_cap_change_percentage_24h']:.2f}%"
    )
    st.badge(f'{ultimo_mercado["market_category"]}', color="primary")

with col4:
    st.metric(
        "Drawdown",
        f"{ultimo_historico['drawdown']:.2f}%"
    )
    

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Distância do ATH",
        f"{ultimo_mercado['ath_distance_pct']:,.2f}%"
    )

with col6:
    st.metric(
        f"Distância do MA {periodo}",
        f"{ultimo_historico[f'ma_distance_{periodo}']:.2f}%"
    )

with col7:
    st.metric(
        "Volume Relativo",
        f"{formatar_numero(ultimo_historico[f'relative_volume_{periodo}'])}x",
    )

with col8:
    st.metric(
        "Volatilidade",
        f"{ultimo_historico[f'volatility_{periodo}']:.2f}%",
    )

grafico_historico = criar_grafico_preco(historico_moeda, periodo, moeda)

col1_grafico, col2_grafico = st.columns([2, 1], gap="large")

with col1_grafico:
    st.plotly_chart(grafico_historico, use_container_width=True)