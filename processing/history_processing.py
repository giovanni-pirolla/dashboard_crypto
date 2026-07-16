import pandas as pd
import numpy as np

JANELAS = [7, 30, 90]

def processar_historico(df_historico: pd.DataFrame):
    # Aqui serão calculadas métricas relacionadas ao histórico de preço das moedas
    
    # Retorno Diário
    df_historico["daily_return"] = df_historico["price"].pct_change() * 100
    
    # Retorno Acumulado ao longo do tempo
    preco_inicial = df_historico['price'].iloc[0]
    df_historico['cumulative_return'] = ((df_historico['price'] - preco_inicial) / preco_inicial) * 100
    
    for janela in JANELAS:
        # Média Móvel
        df_historico[f'ma{janela}'] = df_historico['price'].rolling(window=janela).mean()
        
        # Volatilidade
        df_historico[f'volatility_{janela}'] = df_historico['daily_return'].rolling(window=janela).std()
        
        # Volume Médio
        df_historico[f'avg_volume_{janela}'] = df_historico['volume'].rolling(window=janela).mean()
        
        # Volume Relativo
        df_historico[f'relative_volume_{janela}'] = df_historico['volume'] / df_historico[f'avg_volume_{janela}']
        
        # Drawdown
        maior_preco_historico = df_historico['price'].cummax()
        df_historico['drawdown'] = (df_historico['price'] - maior_preco_historico) / maior_preco_historico * 100
     