import pandas as pd

ESCALAS = [
    (1_000_000_000_000, "T"),
    (1_000_000_000, "B"),
    (1_000_000, "M"),
    (1_000, "K"),
]

def formatar_numero(numero):
    if pd.isna(numero):
        return "N/D"

    for divisor, sufixo in ESCALAS:
        if abs(numero) >= divisor:
            return f"{numero/divisor:,.2f}{sufixo}"

    return f"{numero:,.2f}"

def formatar_tabela(df):
    df_formatado = df.copy()
    
    df_formatado['Preço (USD)'] = df_formatado['Preço (USD)'].apply(formatar_numero)
    df_formatado['Moeda'] = df_formatado['Moeda'].str.upper()
        
    return df_formatado

def colorir_retorno(valor):
    if valor > 0:
        return "color: #22c55e;"   # verde
    elif valor < 0:
        return "color: #ef4444;"   # vermelho
    return "color: #9ca3af;"