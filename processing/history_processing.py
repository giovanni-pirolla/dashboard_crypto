import pandas as pd
import numpy as np

JANELAS = [7, 30, 90]

ESCALAS = [
    (1_000_000_000_000, "T"),
    (1_000_000_000, "B"),
    (1_000_000, "M"),
    (1_000, "K"),
]

def formatar_numero(numero):
    for divisor, sufixo in ESCALAS:
        if numero >= divisor:
            return f'{(numero/divisor):,.2f}{sufixo}'
    
    return f"{numero:,.2f}"

def processar_historico(df_historico: pd.DataFrame):
    # Aqui serão calculadas métricas relacionadas ao histórico de preço das moedas
    
    if df_historico.empty:
        print('O DataFrame de histórico está vazio. Nenhum processamento será realizado.')
        return df_historico
    
    # Retorno Diário
    df_historico['daily_return'] = df_historico['price'].pct_change() * 100
    
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
     
    for janela in JANELAS:
    # Tendência de Preço (usando a hierarquia das médias móveis)
        condicoes_tendencia = [
            ((df_historico['price'] > df_historico['ma7']) & (df_historico['ma7'] > df_historico['ma30']) & (df_historico['ma30'] > df_historico['ma90'])),
            ((df_historico['price'] > df_historico['ma30']) & (df_historico['ma30'] > df_historico['ma90'])),
            ((df_historico['price'] < df_historico['ma7']) & (df_historico['ma7'] < df_historico['ma30']) & (df_historico['ma30'] < df_historico['ma90'])),
            ((df_historico['price'] < df_historico['ma30']) & (df_historico['ma30'] < df_historico['ma90']))
        ]
        escolhas_tendencia = ['Forte Alta', 'Alta', 'Forte Baixa', 'Baixa']
        df_historico['price_trend'] = np.select(condicoes_tendencia, escolhas_tendencia, default='Consolidação')
        
    df_historico["price_diff"] = df_historico["price"].diff()    
    
    # Coluna de Volume Formatada
    df_historico['formatted_volume'] = df_historico['volume'].apply(formatar_numero)
        
    return df_historico