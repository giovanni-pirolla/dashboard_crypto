import pandas as pd
import streamlit as st

from utils.formatting import formatar_numero


def _ausente(valor) -> bool:
    return valor is None or bool(pd.isna(valor))


def _formatar(valor, formatador, padrao="N/D") -> str:
    """Aplica o formatador, ou devolve o padrão quando o valor não existe (None/NaN)."""
    if _ausente(valor):
        return padrao
    return formatador(valor)


def _preco(valor: float) -> str:
    # Moedas de preço baixo precisam de mais casas decimais para não aparecerem como $0.00
    return f"${valor:,.2f}" if abs(valor) >= 1 else f"${valor:,.6f}"


def _data(valor) -> str:
    if _ausente(valor):
        return "N/D"
    try:
        return pd.to_datetime(valor).strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return "N/D"


def montar_metricas_extras(
    ultimo_historico: pd.Series,
    ultimo_mercado: pd.Series,
    periodo: int,
    unidade: str = "",
    intraday: bool = False,
    volume_medio_7d=None,
) -> list[tuple[str, str, str]]:
    """
    Retorna uma lista de (ícone, nome, valor) com as métricas que não aparecem nos cards do topo.
    Os ícones usam a sintaxe nativa do Streamlit (:material/nome:), sem precisar carregar fontes.
    As 6 primeiras são de mercado/volume e as 6 últimas são de preço/supply.
    """

    # Intensidade da variação diária (vem do market_processing)
    nivel = ultimo_mercado.get("change_level")
    variacao = ultimo_mercado.get("change_24h")

    if _ausente(nivel) or _ausente(variacao):
        intensidade = _formatar(nivel, str)
    else:
        intensidade = f"{nivel} ({variacao:+.2f}%)"

    # Volume médio: no modo 24h, usa a média diária de 7 dias; nos demais, a média da janela
    if intraday:
        nome_volume_medio = "Volume Médio Diário (7 dias)"
        volume_medio = volume_medio_7d
    else:
        nome_volume_medio = f"Volume Médio ({periodo} dias)"
        volume_medio = ultimo_historico.get(f"avg_volume_{periodo}")

    simbolo_moeda = str(ultimo_mercado.get("symbol", "")).upper()

    # ATH: preço + data
    ath = ultimo_mercado.get("ath")
    valor_ath = (
        "N/D" if _ausente(ath)
        else f"{_preco(ath)} em {_data(ultimo_mercado.get('ath_date'))}"
    )

    return [
        # --- Mercado e volume ---
        (":material/leaderboard:", "Ranking por Market Cap",
            _formatar(ultimo_mercado.get("rank"), lambda v: f"#{int(v)}")),
        (":material/thermostat:", "Intensidade da Variação (24h)", intensidade),
        (":material/account_balance:", "Variação do Market Cap (24h)",
            _formatar(ultimo_mercado.get("market_cap_change_percentage_24h"), lambda v: f"{v:+.2f}%")),
        (":material/bar_chart:", "Volume 24h",
            _formatar(ultimo_mercado.get("volume"), lambda v: f"${formatar_numero(v)}")),
        (":material/equalizer:", nome_volume_medio,
            _formatar(volume_medio, lambda v: f"${formatar_numero(v)}")),
        (":material/show_chart:", f"Média Móvel ({periodo}{unidade})",
            _formatar(ultimo_historico.get(f"ma{periodo}"), _preco)),

        # --- Preço e supply ---
        (":material/arrow_upward:", "Máxima 24h",
            _formatar(ultimo_mercado.get("high_24h"), _preco)),
        (":material/arrow_downward:", "Mínima 24h",
            _formatar(ultimo_mercado.get("low_24h"), _preco)),
        (":material/landscape:", "Máxima Histórica (ATH)", valor_ath),
        (":material/vertical_align_bottom:", "Distância do ATL",
            _formatar(ultimo_mercado.get("atl_distance_pct"), lambda v: f"{v:+,.2f}%")),
        (":material/toll:", "Supply Circulante",
            _formatar(ultimo_mercado.get("circulating_supply"), lambda v: f"{formatar_numero(v)} {simbolo_moeda}")),
        (":material/pie_chart:", "Supply Máximo em Circulação",
            _formatar(ultimo_mercado.get("supply_pct"), lambda v: f"{v:.2f}%", padrao="N/D (sem supply máximo)")),
    ]


def exibir_metricas_extras(metricas: list[tuple[str, str, str]], colunas: int = 2):
    """Exibe as métricas como linhas de texto, divididas em colunas (preenchidas de cima para baixo)."""
    por_coluna = -(-len(metricas) // colunas)  # divisão com arredondamento para cima
    areas = st.columns(colunas, gap="large")

    for i, area in enumerate(areas):
        with area:
            for simbolo, nome, valor in metricas[i * por_coluna:(i + 1) * por_coluna]:
                valor_seguro = valor.replace("$", r"\$")
                st.markdown(f"{simbolo} **{nome}:** {valor_seguro}")