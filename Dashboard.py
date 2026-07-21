import streamlit as st
import pandas as pd
from services.coingecko import buscar_moedas, buscar_historico_moeda, buscar_dados_mercado
from plots.history_prices import criar_grafico_preco
from processing.history_processing import processar_historico
from processing.market_processing import processar_dados_mercado
from processing.summary_processing import gerar_resumo
    
# Existem mais de 5000 moedas registradas na API do coingecko, por esse motivo, optei por trabalhar apenas com as 12 mais conhecidas
# para evitar qualquer tipo de problema de performance ou desempenho do sistema pelo excesso de registros. Além disso, a versão gratuita da
# API do coingecko permite apenas um número limitado de requisições por minuto, o que impossibilita mais moedas exibidas ao mesmo tempo do 
# que essas
principais_moedas = {
    'bitcoin': 'Bitcoin',
    'ethereum': 'Ethereum',
    'solana': 'Solana',
    'binancecoin': 'BNB',
    'cardano': 'Cardano'
}

st.title('Dashboard de Criptomoedas')

moedas = buscar_moedas()

historico_moedas = buscar_historico_moeda('bitcoin', 90)
historico_moedas = processar_historico(historico_moedas)
dados_mercado = buscar_dados_mercado(['bitcoin', 'ethereum'])
dados_mercado = processar_dados_mercado(dados_mercado, historico_moedas)
resumo_moedas = gerar_resumo(historico_moedas, dados_mercado)

grafico_historico = criar_grafico_preco(historico_moedas, 90)

col1, col2, col3, col4 = st.columns(4)

st.plotly_chart(grafico_historico, use_container_width=True)

