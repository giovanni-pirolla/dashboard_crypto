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