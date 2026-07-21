import pandas as pd
from processing.history_processing import formatar_numero

def gerar_resumo(df_historico: pd.DataFrame, df_mercado: pd.DataFrame):
    ultimo_historico = df_historico.iloc[-1]
    ultimo_mercado = df_mercado.iloc[-1]

    resumo = {
        # Histórico
        "price": ultimo_historico["price"],
        "price_fmt": f"${ultimo_historico['price']:,.2f}",

        "daily_return": ultimo_historico["daily_return"],
        "daily_return_fmt": f"{ultimo_historico['daily_return']:.2f}%",

        "cumulative_return": ultimo_historico["cumulative_return"],
        "cumulative_return_fmt": f"{ultimo_historico['cumulative_return']:.2f}%",

        "drawdown": ultimo_historico["drawdown"],
        "drawdown_fmt": f"{ultimo_historico['drawdown']:.2f}%",

        "price_trend": ultimo_historico["price_trend"],

        "price_diff": ultimo_historico["price_diff"],
        "price_diff_fmt": f"${ultimo_historico['price_diff']:,.2f}",

        # Mercado
        "market_cap": ultimo_mercado["market_cap"],
        "market_cap_fmt": formatar_numero(ultimo_mercado["market_cap"]),

        "rank": ultimo_mercado["rank"],

        "volume": ultimo_mercado["volume"],
        "volume_fmt": formatar_numero(ultimo_mercado["volume"]),

        "change_24h": ultimo_mercado["change_24h"],
        "change_24h_fmt": f"{ultimo_mercado['change_24h']:.2f}%",

        "ath": ultimo_mercado["ath"],
        "ath_fmt": f"${ultimo_mercado['ath']:,.2f}",

        "ath_distance_pct": ultimo_mercado["ath_distance_pct"],
        "ath_distance_pct_fmt": f"{ultimo_mercado['ath_distance_pct']:.2f}%",

        "atl": ultimo_mercado["atl"],
        "atl_fmt": f"${ultimo_mercado['atl']:,.2f}",

        "atl_distance_pct": ultimo_mercado["atl_distance_pct"],
        "atl_distance_pct_fmt": f"{ultimo_mercado['atl_distance_pct']:.2f}%",

        "market_category": ultimo_mercado["market_category"],

        "change_level": ultimo_mercado["change_level"],

        "circulating_supply": ultimo_mercado["circulating_supply"],
        "circulating_supply_fmt": formatar_numero(ultimo_mercado["circulating_supply"]),

        "max_supply": ultimo_mercado["max_supply"],
        "max_supply_fmt": formatar_numero(ultimo_mercado["max_supply"]),

        "supply_pct": ultimo_mercado["supply_pct"],
        "supply_pct_fmt": f"{ultimo_mercado['supply_pct']:.2f}%"
    }

    for janela in [7, 30, 90]:
        resumo[f"ma{janela}"] = ultimo_historico[f"ma{janela}"]
        resumo[f"ma{janela}_fmt"] = f"${ultimo_historico[f'ma{janela}']:,.2f}"

        resumo[f"volatility_{janela}"] = ultimo_historico[f"volatility_{janela}"]
        resumo[f"volatility_{janela}_fmt"] = f"{ultimo_historico[f'volatility_{janela}']:.2f}%"

        resumo[f"avg_volume_{janela}"] = ultimo_historico[f"avg_volume_{janela}"]
        resumo[f"avg_volume_{janela}_fmt"] = formatar_numero(
            ultimo_historico[f"avg_volume_{janela}"]
        )

        resumo[f"relative_volume_{janela}"] = ultimo_historico[f"relative_volume_{janela}"]
        resumo[f"relative_volume_{janela}_fmt"] = (
            f"{ultimo_historico[f'relative_volume_{janela}']:.2f}x"
        )

    return resumo