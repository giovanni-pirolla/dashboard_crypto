import requests
import pandas as pd  
import datetime as dt

BASE_URL = 'https://api.coingecko.com/api/v3'

COLUNAS_MERCADO = [
    "id",
    "symbol",
    "name",
    "image",
    "current_price",
    "market_cap",
    "market_cap_rank",
    "total_volume",
    "high_24h",
    "low_24h",
    "price_change_percentage_24h",
    "circulating_supply",
    "total_supply",
    "max_supply",
    "ath",
    "ath_change_percentage",
    "ath_date",
    "atl",
    "atl_change_percentage",
    "atl_date",
    "last_updated"
]

RENOMEAR_COLUNAS_MERCADO = {
    "image": "image_url",
    "current_price": "price",
    "market_cap_rank": "rank",
    "total_volume": "volume",
    "price_change_percentage_24h": "change_24h",
    "ath_change_percentage": "ath_change_pct",
    "atl_change_percentage": "atl_change_pct",
    "last_updated": "updated_at",
}

#função genérica para ser utilizada em todas as requisições
def buscar_dados_da_api(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        print('Sucesso')
        return pd.DataFrame(response.json())
    except Exception as e:
        print(f'Erro de Conexão com a API: {e}')
        return pd.DataFrame()
        

def buscar_moedas():
    url = f"{BASE_URL}/coins/list"

    df = buscar_dados_da_api(url)
    
    return df

def buscar_historico_moeda(id_moeda: str, dias: int):
    url = f'{BASE_URL}/coins/{id_moeda}/market_chart?vs_currency=usd&days={dias}'
    
    df = buscar_dados_da_api(url)
    
    for col in df.columns:
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
            'timestamp_prices' : 'date',
            'total_volumes' : 'volume',
            'market_caps' : 'market_cap'
        }
    )
    
    df = df.sort_values("date")
    
    df = df[['date', 'prices', 'market_cap', 'volume']]
    
    return df

def buscar_candles_moeda(id_moeda: str, dias: int):
    url = f'{BASE_URL}/coins/{id_moeda}/ohlc?vs_currency=usd&days={dias}'
    
    df = buscar_dados_da_api(url)
    
    df.columns = [
        "date",
        "open",
        "high",
        "low",
        "close"
    ]
    
    df['date'] = pd.to_datetime(
        df['date'],
        unit='ms'
    )
    
    return df

def buscar_dados_mercado(ids_moedas: list[str]):
    if not ids_moedas:
        print('Lista de moedas inválida')
        return pd.DataFrame()
        
    ids = ",".join(ids_moedas)
    url = f'{BASE_URL}/coins/markets?vs_currency=usd&ids={ids}'
    
    df = buscar_dados_da_api(url)
    
    df = df[COLUNAS_MERCADO]
    df = df.rename(columns=RENOMEAR_COLUNAS_MERCADO)
    
    return df

# bitcoin = buscar_historico_moeda('bitcoin', 1)

# moedas = buscar_moedas()

# bitcoin_candles = buscar_candles_moeda('bitcoin', 1)
# print(bitcoin_candles)

dados_mercado = buscar_dados_mercado(['bitcoin', 'ethereum'])
print(dados_mercado)