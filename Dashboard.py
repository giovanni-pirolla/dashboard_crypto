import streamlit as st
import pandas as pd
from services.coingecko import buscar_moedas, buscar_historico_moeda, buscar_candles_moeda, buscar_dados_mercado
from plots.candles import criar_grafico_candles

# Existem mais de 5000 moedas registradas na API do coingecko, por esse motivo, optei por trabalhar apenas com as 12 mais conhecidas
# para evitar qualquer tipo de problema de performance ou desempenho do sistema pelo excesso de registros. Além disso, a versão gratuita da
# API do coingecko permite apenas um número limitado de requisições por minuto, o que impossibilita mais moedas exibidas ao mesmo tempo do 
# que essas
principais_moedas = {
    "bitcoin": "Bitcoin",
    "ethereum": "Ethereum",
    "solana": "Solana",
    "binancecoin": "BNB",
    "cardano": "Cardano"
}

moedas = buscar_moedas()
historico_moedas = buscar_historico_moeda("bitcoin", 30)
candles_moedas = buscar_candles_moeda("bitcoin", 30)
dados_mercado = buscar_dados_mercado(["bitcoin", "ethereum"])

grafico_candles = criar_grafico_candles(candles_moedas, historico_moedas)

st.plotly_chart(grafico_candles, use_container_width=True)

