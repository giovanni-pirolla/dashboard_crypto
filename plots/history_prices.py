import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

CORES_MEDIAS = {
    7: "rgba(59,130,246,0.75)",
    30: "rgba(245,158,11,0.75)",
    90: "rgba(168,85,247,0.75)"
}


def criar_grafico_preco(df_historico: pd.DataFrame, dias: int):
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.85, 0.15],
        vertical_spacing=0.05
    )
    
    ultimo_movimento = df_historico["price_diff"].iloc[-1]
    
    if ultimo_movimento >= 0:
        cor_linha = "#22C55E"
        cor_preenchimento = "rgba(34,197,94,0.15)"
        cor_tracado = "rgba(34, 197, 94, 0.70)"
    else:
        cor_linha = "#EF4444"
        cor_preenchimento = "rgba(239,68,68,0.15)"
        cor_tracado = "rgba(239, 68, 68, 0.70)"

    fig.add_trace(
        go.Scatter(
            x=df_historico["date"],
            y=df_historico["price"],
            mode="lines",
            name="Preço",
            line=dict(
                color=cor_linha,
                width=2
            ),
            fill="tozeroy",
            fillcolor=cor_preenchimento,
            customdata=df_historico[["price"]],
            hovertemplate=
            "<br><b>Preço</b><br>"
            "$%{customdata[0]:,.2f}"
            "<extra></extra>"
        ),
        row=1,
        col=1
    )

    for janela, cor in CORES_MEDIAS.items():
        if janela >= dias:
            continue

        fig.add_trace(
            go.Scatter(
                x=df_historico["date"],
                y=df_historico[f"ma{janela}"],
                mode="lines",
                name=f"MA {janela}",
                line=dict(
                    color=cor,
                    width=2
                ),
                meta=janela,
                customdata=df_historico[[f"ma{janela}"]],
                hovertemplate=
                "<br><b>MA %{meta}</b><br>"
                "$%{customdata[0]:,.2f}"
                "<extra></extra>"
            ),
            row=1,
            col=1
        )

    cores_volume = ["#22C55E" if variacao >= 0 else "#EF4444" for variacao in df_historico["price"].diff().fillna(0)]

    fig.add_trace(
        go.Bar(
            x=df_historico["date"],
            y=df_historico["volume"],
            marker_color=cores_volume,
            name="Volume",
            customdata=df_historico[["formatted_volume"]],
            hovertemplate=
            "<br><b>Volume</b><br>"
            "%{customdata[0]} USD"
            "<extra></extra>",
            showlegend=False
        ),
        row=2,
        col=1
    )
    
    fig.add_hline(
        y=df_historico['price'].iloc[-1],
        line_dash="dash",
        line_color=cor_tracado,
        annotation_text=f"<b>${df_historico['price'].iloc[-1]:,.2f}<b>",
        annotation_position="top right",
        annotation_font=dict(
            color=cor_tracado,
            size=13
        ),
        annotation_yshift=+5,
        row=1,
        col=1
    )

    fig.update_traces(
        hoverlabel=dict(
            bgcolor="black",
            font_size=14
        )
    )

    fig.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(
            family="Arial",
            size=14,
            color="white"
        ),
        hovermode="x unified",
        yaxis_title="Preço (USD)",
        xaxis=dict(
            unifiedhovertitle=dict(
                text="<b>%{x|%d/%m/%Y}</b>"
            )
        ),
        showlegend=True
    )

    fig.update_xaxes(
        title_text="Data",
        row=2,
        col=1,
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(255,255,255,0.10)",
        showline=True,
        linewidth=1,
        linecolor="rgba(255,255,255,0.10)",
        tickformat="%d/%m"
    )

    fig.update_yaxes(
        title_text="Preço (USD)",
        row=1,
        col=1,
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(255,255,255,0.10)",
        showline=True,
        linewidth=1,
        linecolor="rgba(255,255,255,0.10)"
    )

    fig.update_yaxes(
        title_text="Volume",
        row=2,
        col=1,
        showticklabels=False,
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(255,255,255,0.10)",
        showline=True,
        linewidth=1,
        linecolor="rgba(255,255,255,0.10)"
    )

    return fig