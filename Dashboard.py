import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import time

# O Streamlit reexecutava o código a cada vez que o usuário selecionava uma moeda, por isso utilizei o cache_data para evitar essa 
# reexecução desnecessária
@st.cache_data(ttl=3600)
def buscar_moedas():
    url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
    return None

moedas = buscar_moedas()

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

moedas = moedas.set_index('id')
moedas = moedas.loc[list(principais_moedas.keys())]
    
# Estrutura principal do App, onde o usuário escolhe as moedas e o período de tempo desejado para a análise da volatilidade
st.title('Verificador de Volatidade de CryptoMoedas')

st.sidebar.title('Personalize sua experiência')
moedas_selecionadas = st.sidebar.multiselect(label='Moedas Selecionadas:', options= list(principais_moedas.values()), default="Bitcoin")

id_moedas = []
for id_moeda, nome_moeda in principais_moedas.items():
    if nome_moeda in moedas_selecionadas:
        id_moedas.append(id_moeda)

periodo_selecionado = st.sidebar.number_input(label='Selecione o período em dias desejado para a análise', step=1)
moedas = moedas[moedas['name'].isin(moedas_selecionadas)]

# Função para retornar o histórico de cada moeda
@st.cache_data(ttl=3600)
def buscar_historico(id_moeda, dias):
    url = f"https://api.coingecko.com/api/v3/coins/{id_moeda}/market_chart?vs_currency=usd&days={dias}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return pd.DataFrame.from_dict(response.json())
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
    return pd.DataFrame()


for moeda in id_moedas:
    
    with st.container():
            st.subheader(f"Dados de {principais_moedas[moeda]}")
            
            with st.spinner(f"Buscando dados de {principais_moedas[moeda]}..."):
                df = buscar_historico(moeda, periodo_selecionado)
                
                if not df.empty:
                    st.dataframe(df)
                
    
