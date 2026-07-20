import pandas as pd

# Constantes para Intensidade da Variação 
QUEDA_ACENTUADA = -10
QUEDA_MODERADA = -3
ALTA_MODERADA = 3
ALTA_FORTE = 10

# Constantes para Faixa de Mercado
BIG_CAP = 1e10
SMALL_CAP = 2e10

def processar_dados_mercado(df_mercado: pd.DataFrame, df_historico: pd.DataFrame):
    # Aqui, serão calculadas métricas úteis para traders com base nas informações gerais sobre cada moeda, que serão exibidas em cards no dashboard
    
    # Distância até o ATH
    df_mercado['ath_distance_pct'] = (df_mercado['price'] - df_mercado['ath'])/df_mercado['ath'] * 100
    
    # Distância até o ATL
    df_mercado['atl_distance_pct'] = (df_mercado['price'] - df_mercado['atl'])/df_mercado['atl'] * 100
    
    # Percentual de Supply
    df_mercado['supply_pct'] = (df_mercado['circulating_supply'] / df_mercado['max_supply']) * 100
    
    # Faixa de Mercado 
    df_mercado['market_category'] = df_historico['market_cap'].apply(lambda market_cap: (
        'Big Cap' if market_cap >= BIG_CAP
        else 'Mid Cap' if market_cap >= SMALL_CAP
        else 'Small Cap'
        ))
    
    # Intensidade da Variação Diária
    df_mercado['change_level'] = df_mercado['change_24h'].apply(
        lambda variacao:
            'Queda Acentuada' if variacao <= QUEDA_ACENTUADA else
            'Queda Moderada' if variacao <= QUEDA_MODERADA else
            'Estável' if variacao < ALTA_MODERADA else
            'Alta Moderada' if variacao < ALTA_FORTE else
            'Alta Forte'
    )
    
    return df_mercado