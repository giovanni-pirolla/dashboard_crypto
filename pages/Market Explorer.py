import streamlit as st
import pandas as pd

from services.coingecko import buscar_todos_dados_mercado
from utils.formatting import formatar_tabela, colorir_retorno, formatar_numero

# Título e descrição da página
st.title("Market Explorer")
st.subheader('Explore o ranking de criptomoedas através de filtros customizados.')

st.divider()

todos_dados_mercado = buscar_todos_dados_mercado()

filtros, grafico = st.expander("Filtros de Pesquisa", expanded=True), st.expander("Ranking de CriptoMoedas", expanded=True)


# Filtros 
with filtros:
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        NUMERO_MOEDAS = st.number_input(
            "Número de CriptoMoedas a serem exibidas",
            min_value=1,
            max_value=100,
            value=10,
            step=1
        )
        
        NOME_MOEDA = st.text_input("Nome ou Código da Moeda a ser Analisada", value="")
        
    with col2:
        preco_max = float(todos_dados_mercado["current_price"].max())
        
        INTERVALO_VALOR = st.slider(
            "Intervalo de Valor (USD)",
            min_value=0.0,
            max_value=preco_max,
            value=(0.0, preco_max),
            format="$%.2f",
            step=1.0
        )
        
        opcoes_market_cap = [0, 1e6, 1e7, 1e8, 1e9, 1e10, 1e11, 1e12, 2e12]

        INTERVALO_MARKET_CAP = st.select_slider(
            "Intervalo de Market Cap (USD)",
            options=opcoes_market_cap,
            value=(opcoes_market_cap[0], opcoes_market_cap[-1]),
            format_func=lambda n: f"${formatar_numero(n)}",
        )

        mc_min, mc_max = INTERVALO_MARKET_CAP

    with col3:
        ORDENAR_POR = st.selectbox(
            "Ordenar por",
            options=[
                "Market Cap",
                "Preço (USD)",
                "Retorno Diário",
                "Volume Total",
                "Mudança de Market Cap (24h)"
            ],
            index=0
        )
        
        ORDEM = st.selectbox(
            "Ordem",
            options=["Decrescente", "Crescente"],
            index=0
        )
        
        MAPEAR_ORDENACAO = {
            "Crescente": True,
            "Decrescente": False
        }

def aplicar_filtros(df, nome, intervalo_valor, intervalo_market_cap, ordenar_por, numero_moedas):
    df_filtrado = df.copy()

    # 1) Filtro por nome ou símbolo 
    if nome.strip():
        termo = nome.strip()
        mascara_nome = (
            df_filtrado["Nome"].str.contains(termo, case=False, na=False, regex=False)
            | df_filtrado["Moeda"].str.contains(termo, case=False, na=False, regex=False)
        )
        df_filtrado = df_filtrado[mascara_nome]

    # 2) Filtro por intervalo de preço
    valor_min, valor_max = intervalo_valor
    df_filtrado = df_filtrado[
        df_filtrado["Preço (USD)"].between(valor_min, valor_max)
    ]

    # 3) Filtro por intervalo de market cap
    market_cap_min, market_cap_max = intervalo_market_cap
    df_filtrado = df_filtrado[
        df_filtrado["Market Cap"].between(market_cap_min, market_cap_max)
    ]

    # 4) Ordenação (maior para menor; NaN vão para o final
    df_filtrado = df_filtrado.sort_values(ordenar_por, ascending=MAPEAR_ORDENACAO[ORDEM], na_position="last")
    
    df_filtrado = df_filtrado[df_filtrado["Market Cap"].between(mc_min, mc_max)]

    # 5) Limite de linhas (sempre por último)
    return df_filtrado.head(numero_moedas)


# Carregamento dos dados do mercado
with grafico:
    df_tabela = todos_dados_mercado[
        ["image", "symbol", "name", "current_price", "price_change_percentage_24h",
         "market_cap", "total_volume", "market_cap_change_percentage_24h"]
    ].rename(
        columns={
            "symbol": "Moeda",
            "name": "Nome",
            "current_price": "Preço (USD)",
            "price_change_percentage_24h": "Retorno Diário",
            "market_cap": "Market Cap",
            "total_volume": "Volume Total",
            "market_cap_change_percentage_24h": "Mudança de Market Cap (24h)",
        }
    )

    # Filtra ANTES de formatar
    df_tabela = aplicar_filtros(
        df_tabela,
        nome=NOME_MOEDA,
        intervalo_valor=INTERVALO_VALOR,
        intervalo_market_cap=INTERVALO_MARKET_CAP,
        ordenar_por=ORDENAR_POR,
        numero_moedas=NUMERO_MOEDAS,
    )

    if df_tabela.empty:
        st.info("Nenhuma criptomoeda encontrada com os filtros selecionados.")
    else:
        df_tabela = formatar_tabela(df_tabela)

        df_estilizado = (
            df_tabela.style
            .format({
                "Preço (USD)": formatar_numero,
                "Retorno Diário": "{:+.2f}%",
                "Market Cap": formatar_numero,
                "Volume Total": formatar_numero,
                "Mudança de Market Cap (24h)": "{:+.2f}%",
            })
            .map(colorir_retorno, subset=["Retorno Diário", "Mudança de Market Cap (24h)"])
            .set_properties(**{"font-weight": "bold"})
            .set_table_styles([
                {"selector": "th", "props": [("font-weight", "bold"), ("font-size", "15px")]}
            ])
        )

        st.dataframe(
            df_estilizado,
            column_config={
                "image": st.column_config.ImageColumn("Ícone", width="small")
            },
            use_container_width=True,
            hide_index=True,
        )