import pandas as pd

def processar_historico(df_historico: pd.DataFrame):
    # Aqui serão calculadas métricas relacionadas ao histórico de preço das moedas
    
    # Retorno Diário
    df_historico["daily_return"] = df_historico["price"].pct_change() * 100
    
    # Retorno Acumulado
    preco_inicial = df_historico['price'].iloc[0]
    preco_atual = df_historico['price'].iloc[-1]
    df_historico['all_time_return'] = ((preco_atual - preco_inicial) / preco_inicial) * 100
    
    # Médias Móveis
    