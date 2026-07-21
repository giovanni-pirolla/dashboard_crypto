import requests
import pandas as pd  
import datetime as dt
import streamlit as st

BASE_URL = 'https://api.coingecko.com/api/v3'

COLUNAS_MERCADO = [
    'id',
    'symbol',
    'name',
    'image',
    'current_price',
    'market_cap',
    'market_cap_rank',
    'market_cap_change_24h',
    'market_cap_change_percentage_24h',
    'total_volume',
    'high_24h',
    'low_24h',
    'price_change_percentage_24h',
    'circulating_supply',
    'total_supply',
    'max_supply',
    'ath',
    'ath_change_percentage',
    'ath_date',
    'atl',
    'atl_change_percentage',
    'atl_date',
    'last_updated'
]

RENOMEAR_COLUNAS_MERCADO = {
    'image': 'image_url',
    'current_price': 'price',
    'market_cap_rank': 'rank',
    'total_volume': 'volume',
    'price_change_percentage_24h': 'change_24h',
    'ath_change_percentage': 'ath_change_pct',
    'atl_change_percentage': 'atl_change_pct',
    'last_updated': 'updated_at',
}

#função genérica para ser utilizada em todas as requisições
def buscar_dados_da_api(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        return pd.DataFrame(response.json())
    
    except requests.HTTPError as e:
        print(f'Erro HTTP: {e}')
        return None

    except requests.RequestException as e:
        print(f'Erro de conexão: {e}')
        return None
        
@st.cache_data(ttl=86400)
def buscar_moedas():
    url = f'{BASE_URL}/coins/list'

    df = buscar_dados_da_api(url)
    if df is None:
        return pd.DataFrame()
    
    return df

@st.cache_data(ttl=86400)
def buscar_mapeamento_moedas():
    df_moedas = buscar_moedas()

    return dict(
        zip(
            df_moedas["id"],
            df_moedas["name"]
        )
    )

@st.cache_data(ttl=300)
def buscar_historico_moeda(id_moeda: str, dias: int):
    interval = 'daily'
    
    url = f'{BASE_URL}/coins/{id_moeda}/market_chart?vs_currency=usd&days={dias}&interval={interval}'
    
    df = buscar_dados_da_api(url)
    if df is None:
        return pd.DataFrame()
    
    for col in ['prices','market_caps','total_volumes']:
        df[[f'timestamp_{col}', col]] = pd.DataFrame(
            df[col].to_list(),
            index=df.index
        )
    
    df['timestamp_prices'] = pd.to_datetime(
        df['timestamp_prices'],
        unit='ms'
    )
    
    df = df.drop(
        columns=[
            'timestamp_market_caps',
            'timestamp_total_volumes'
        ]
    )
    
    df = df.rename(
        columns={
            'prices' : 'price',
            'timestamp_prices' : 'date',
            'total_volumes' : 'volume',
            'market_caps' : 'market_cap'
        }
    )
    
    df['date'] = df['date'].dt.date
    df = df.drop_duplicates('date', keep='last')
    
    return df

@st.cache_data(ttl=60)
def buscar_dados_mercado(id_moeda: str):
    if not id_moeda:
        print('Lista de moedas inválida')
        return pd.DataFrame()
        
    url = f'{BASE_URL}/coins/markets?vs_currency=usd&ids={id_moeda}'
    
    df = buscar_dados_da_api(url)
    if df is None:
        return pd.DataFrame()
    
    df = df[COLUNAS_MERCADO]
    df = df.rename(columns=RENOMEAR_COLUNAS_MERCADO)
    
    return df