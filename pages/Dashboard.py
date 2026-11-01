import streamlit as st

from services.coingecko import (
    buscar_moedas,
    buscar_historico_moeda,
    buscar_historico_intraday,
    buscar_dados_mercado,
    buscar_mapeamento_moedas,
    buscar_todos_dados_mercado
)

from plots.history_prices import criar_grafico_preco
from plots.intraday_history import criar_grafico_intraday
from processing.history_processing import processar_historico, JANELAS
from processing.market_processing import processar_dados_mercado
from processing.metric_analysis import (
    analisar_market_cap,
    analisar_volume_relativo,
    analisar_ma,
    analisar_ath,
    analisar_delta
)

from utils.formatting import formatar_numero, formatar_tabela, colorir_retorno
from utils.fonts import carregar_fontes
from components.metrics import montar_metricas_extras, exibir_metricas_extras

carregar_fontes()

st.set_page_config(layout="wide")

st.markdown("# :material/dashboard: Dashboard de Análise de Criptomoedas")
st.space()

# Configurações do modo 24h
OPCAO_24H = "24h"
JANELAS_INTRADAY = [6]  # janelas em horas (os dados são reamostrados para 1 hora)

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
    periodo_selecionado = st.segmented_control(
        "Período",
        [OPCAO_24H] + JANELAS,
        default=[OPCAO_24H],
        format_func=lambda p: p if p == OPCAO_24H else f"{p} dias"
    )

# O segmented_control retorna None se o usuário desmarcar a opção atual
if periodo_selecionado is None:
    periodo_selecionado = 30

intraday = periodo_selecionado == OPCAO_24H

# Carregamento dos dados processados
if intraday:
    periodo = JANELAS_INTRADAY[0]   # 6 (horas)
    unidade = "h"
    rotulo_periodo = "24h"

    # Dados de 5 em 5 minutos, usados no gráfico
    historico_intraday = buscar_historico_intraday(moeda)

    if historico_intraday.empty:
        st.error("Não foi possível carregar os dados das últimas 24h. Tente novamente em instantes.")
        st.stop()

    # Versão horária dos mesmos dados, usada nas métricas
    historico_horario = (
        historico_intraday.set_index("date")
        .resample("1h").last()
        .dropna()
        .reset_index()
    )

    historico_moeda = processar_historico(historico_horario, janelas=JANELAS_INTRADAY)
else:
    periodo = periodo_selecionado
    unidade = ""
    rotulo_periodo = f"{periodo} dias"

    historico_moeda = buscar_historico_moeda(moeda, periodo)

    if historico_moeda.empty:
        st.error("Não foi possível carregar o histórico da moeda. Tente novamente em instantes.")
        st.stop()

    historico_moeda = processar_historico(historico_moeda)

dados_mercado = buscar_dados_mercado(moeda)
dados_mercado = processar_dados_mercado(dados_mercado, historico_moeda)

todos_dados_mercado = buscar_todos_dados_mercado()

ultimo_historico = historico_moeda.iloc[-1]
ultimo_mercado = dados_mercado.iloc[-1]

# No modo 24h, o volume é o acumulado das últimas 24h; compara com a média diária de 7 dias
media_volume_7d = None

if intraday:
    historico_7d = buscar_historico_moeda(moeda, 7)

    if not historico_7d.empty:
        media_volume_7d = historico_7d["volume"].mean()
        ultimo_historico[f"relative_volume_{periodo}"] = ultimo_historico["volume"] / media_volume_7d

# Carregamento das análises das métricas
analise_retorno = analisar_delta(ultimo_historico["daily_return"])
analise_market_cap = analisar_market_cap(ultimo_mercado["market_category"])
analise_volume_relativo = analisar_volume_relativo(ultimo_historico[f"relative_volume_{periodo}"])
analise_ma = analisar_ma(ultimo_historico[f"ma_distance_{periodo}"])
analise_ath = analisar_ath(ultimo_mercado["ath_distance_pct"])
analise_drawdown = analisar_delta(ultimo_historico["drawdown_delta"])
analise_volatilidade = analisar_delta(ultimo_historico[f"volatility_delta_{periodo}"])
analise_retorno_acumulado = analisar_delta(ultimo_historico["cumulative_return_delta"])

if intraday:
    st.caption("Modo 24h: as métricas são calculadas com base nas últimas 24 horas, em janelas horárias.")

st.divider()

# Colunas de Métricas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Preço Atual",
        f"${ultimo_historico['price']:,.2f}"
    )
    st.badge(f"{ultimo_historico['daily_return']:+.2f}%", color=analise_retorno["color"], icon=analise_retorno["icon"])

with col2:
    st.metric(
        f"Retorno Acumulado ({rotulo_periodo})",
        f"{ultimo_historico['cumulative_return']:.2f}%"
    )
    st.badge(f"{ultimo_historico['cumulative_return_delta']:+.2f}%", color=analise_retorno_acumulado["color"], icon=analise_retorno_acumulado["icon"])

with col3:
    st.metric(
        "Market Cap",
        formatar_numero(ultimo_mercado["market_cap"]),
    )
    st.badge(analise_market_cap["label"], color=analise_market_cap["color"], icon=analise_market_cap["icon"])

with col4:
    st.metric(
        "Drawdown",
        f"{ultimo_historico['drawdown']:.2f}%"
    )
    st.badge(f"{ultimo_historico['drawdown_delta']:+.2f}%", color=analise_drawdown["color"], icon=analise_drawdown["icon"])

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Distância do ATH",
        f"{ultimo_mercado['ath_distance_pct']:.2f}%"
    )
    st.badge(analise_ath["label"], color=analise_ath["color"], icon=analise_ath["icon"])

with col6:
    st.metric(
        f"Distância do MA {periodo}{unidade}",
        f"{ultimo_historico[f'ma_distance_{periodo}']:.2f}%"
    )
    st.badge(f"{analise_ma['label']}", color=analise_ma["color"], icon=analise_ma["icon"])

with col7:
    st.metric(
        "Volume Relativo",
        f"{ultimo_historico[f'relative_volume_{periodo}']:.2f}x",
    )
    st.badge(f"{analise_volume_relativo['label']}", color=analise_volume_relativo["color"], icon=analise_volume_relativo["icon"])

with col8:
    st.metric(
        "Volatilidade",
        f"{ultimo_historico[f'volatility_{periodo}']:.2f}%"
    )
    st.badge(f"{ultimo_historico[f'volatility_delta_{periodo}']:+.2f}%", color=analise_volatilidade["color"], icon=analise_volatilidade["icon"])


st.divider()

if intraday:
    grafico_historico = criar_grafico_intraday(historico_intraday, moeda, nomes_moedas)
else:
    grafico_historico = criar_grafico_preco(historico_moeda, periodo, moeda, nomes_moedas)

col_grafico, col_tabela = st.columns([1.80, 1], gap="large")

with col_grafico:
    st.plotly_chart(grafico_historico, use_container_width=True)
    
    st.divider()

    st.subheader("Métricas Complementares", help="Métricas adicionais que fornecem insights sobre a moeda, incluindo volume médio, médias móveis e supply.")
    st.space()

    metricas_extras = montar_metricas_extras(
        ultimo_historico,
        ultimo_mercado,
        periodo,
        unidade,
        intraday,
        media_volume_7d
    )
    exibir_metricas_extras(metricas_extras)

with col_tabela:
    NUMERO_MOEDAS = 10
    
    st.space()

    df_tabela = todos_dados_mercado.copy()

    df_tabela = df_tabela[
        ["image", "name", "current_price", "price_change_percentage_24h"]
    ]

    df_tabela = df_tabela.rename(
        columns={
            "name": "Moeda",
            "current_price": "Preço (USD)",
            "price_change_percentage_24h": "Retorno Diário",
        }
    )

    df_tabela = df_tabela.head(NUMERO_MOEDAS)

    df_tabela = formatar_tabela(df_tabela)

    df_estilizado = (
        df_tabela.style
        .format({
            "Retorno Diário": "{:+.2f}%",
            "Preço (USD)": formatar_numero
        })
        .map(colorir_retorno, subset=["Retorno Diário"])
        .set_properties(**{
            "font-weight": "bold"
        })
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("font-weight", "bold"),
                    ("font-size", "15px"),
                ]
            }
        ])
    )
    

    st.subheader(f"Top {NUMERO_MOEDAS} CriptoMoedas por Market Cap", help="Para uma análise mais detalhada do ranking de moedas, acesse o Market Explorer.")

    st.dataframe(
        df_estilizado,
        column_config={
            "image": st.column_config.ImageColumn(
                "Ícone",
                width="small"
            )
        },
        use_container_width=True,
        hide_index=True
    )
    st.page_link(
        "pages/Market Explorer.py",
        icon=":material/search:",
        label="Explorar Mais Opções de CriptoMoedas",
        use_container_width=True,
    )