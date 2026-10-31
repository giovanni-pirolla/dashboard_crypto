import pandas as pd
import plotly.graph_objects as go

def criar_grafico_intraday(df: pd.DataFrame, moeda: str, nomes_moedas: dict) -> go.Figure:
    # Cor definida pela variação do período todo (primeiro -> último ponto)
    variacao = df["price"].iloc[-1] - df["price"].iloc[0]
 
    if variacao >= 0:
        cor_linha = "#22C55E"
        cor_preenchimento = "rgba(34,197,94,0.15)"
    else:
        cor_linha = "#EF4444"
        cor_preenchimento = "rgba(239,68,68,0.15)"
 
    preco_min, preco_max = df["price"].min(), df["price"].max()
    margem = (preco_max - preco_min) * 0.1 or preco_max * 0.001
 
    fig = go.Figure()
 
    # Trace invisível no mínimo, usado como base do preenchimento (evita forçar o eixo Y até zero)
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=[preco_min - margem] * len(df),
            mode="lines",
            line=dict(width=0),
            hoverinfo="skip",
            showlegend=False
        )
    )
 
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["price"],
            mode="lines",
            name="Preço",
            line=dict(
                color=cor_linha,
                width=3
            ),
            fill="tonexty",
            fillcolor=cor_preenchimento,
            hovertemplate=
            "<br><b>Preço</b><br>"
            "$%{y:,.2f}"
            "<extra></extra>",
            hoverlabel=dict(
                bgcolor="black",
                font_size=14
            )
        )
    )
 
    fig.update_layout(
        title={
            "text": f"Preço nas últimas 24h ({nomes_moedas[moeda]})",
            "font": {
                "size": 24,
                "family": "Inter, sans-serif",
                "color": "white"
            },
        },
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(
            family="Arial",
            size=14,
            color="white"
        ),
        hovermode="x unified",
        height=450,
        showlegend=False,
        xaxis=dict(
            title="Horário",
            tickformat="%H:%M",
            unifiedhovertitle=dict(
                text="<b>%{x|%d/%m %H:%M}</b>"
            ),
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(255,255,255,0.10)",
            showline=True,
            linewidth=1,
            linecolor="rgba(255,255,255,0.10)"
        ),
        yaxis=dict(
            title="Preço (USD)",
            range=[preco_min - margem, preco_max + margem],
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(255,255,255,0.10)",
            showline=True,
            linewidth=1,
            linecolor="rgba(255,255,255,0.10)"
        )
    )
 
    return fig