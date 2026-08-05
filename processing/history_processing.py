import pandas as pd
import numpy as np
from utils.formatting import formatar_numero

JANELAS = [7, 30, 90, 365]

def processar_historico(df_historico: pd.DataFrame):
    if df_historico.empty:
        print("O DataFrame de histórico está vazio. Nenhum processamento será realizado.")
        return df_historico

    df_historico["daily_return"] = df_historico["price"].pct_change() * 100

    preco_inicial = df_historico["price"].iloc[0]
    df_historico["cumulative_return"] = ((df_historico["price"] - preco_inicial) / preco_inicial) * 100
    df_historico["cumulative_return_delta"] = df_historico["cumulative_return"].diff()

    maior_preco_historico = df_historico["price"].cummax()
    df_historico["drawdown"] = ((df_historico["price"] - maior_preco_historico) / maior_preco_historico) * 100
    df_historico["drawdown_delta"] = df_historico["drawdown"].diff()

    for janela in JANELAS:
        df_historico[f"ma{janela}"] = df_historico["price"].rolling(window=janela).mean()
        df_historico[f"ma_distance_{janela}"] = ((df_historico["price"] - df_historico[f"ma{janela}"]) / df_historico[f"ma{janela}"]) * 100
        df_historico[f"ma_distance_delta_{janela}"] = df_historico[f"ma_distance_{janela}"].diff()

        df_historico[f"volatility_{janela}"] = df_historico["daily_return"].rolling(window=janela, min_periods=1).std()
        df_historico[f"volatility_delta_{janela}"] = df_historico[f"volatility_{janela}"].diff()

        df_historico[f"avg_volume_{janela}"] = df_historico["volume"].rolling(window=janela).mean()
        df_historico[f"relative_volume_{janela}"] = df_historico["volume"] / df_historico[f"avg_volume_{janela}"]
        df_historico[f"volume_delta_{janela}"] = ((df_historico["volume"] - df_historico[f"avg_volume_{janela}"]) / df_historico[f"avg_volume_{janela}"]) * 100

    condicoes_tendencia = [
        (df_historico["price"] > df_historico["ma7"]) & (df_historico["ma7"] > df_historico["ma30"]) & (df_historico["ma30"] > df_historico["ma90"]),
        (df_historico["price"] > df_historico["ma30"]) & (df_historico["ma30"] > df_historico["ma90"]),
        (df_historico["price"] < df_historico["ma7"]) & (df_historico["ma7"] < df_historico["ma30"]) & (df_historico["ma30"] < df_historico["ma90"]),
        (df_historico["price"] < df_historico["ma30"]) & (df_historico["ma30"] < df_historico["ma90"])
    ]

    escolhas_tendencia = ["🟢 Forte Alta", "🟢 Alta", "🔴 Forte Baixa", "🔴 Baixa"]

    df_historico["price_trend"] = np.select(condicoes_tendencia, escolhas_tendencia, default="🟡 Consolidação")
    df_historico["price_diff"] = df_historico["price"].diff()
    df_historico["formatted_volume"] = df_historico["volume"].apply(formatar_numero)

    return df_historico