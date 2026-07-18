import pandas as pd
import plotly.graph_objects as go

def criar_grafico_candles(df_candles: pd.DataFrame, df_historico: pd.DataFrame, dias: int):
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Candlestick(
            x=df_candles['date'],
            open=df_candles['open'],
            high=df_candles['high'],
            low=df_candles['low'],
            close=df_candles['close'],
            increasing_line_color='#22C55E',
            decreasing_line_color='#EF4444',
            increasing_fillcolor="#22C55E",
            decreasing_fillcolor="#EF4444",
            name="",
            customdata = df_candles[['direction']],
            hovertemplate=
            '<br><b>%{customdata[0]}</b><br><br>' +
            'Open:     $%{open:,.2f}<br>' +
            'High:       $%{high:,.2f}<br>' +
            'Low:        $%{low:,.2f}<br>' +
            'Close:     $%{close:,.2f}' +
            '<extra></extra>'
            )
    )
    
    for i, janela in enumerate([7,30,90]):
        if janela < dias:
            fig.add_trace(
                go.Scatter(
                    x=df_historico['date'],
                    y=df_historico[f'ma{janela}'],
                    mode='lines',
                    line=dict(color=["rgba(59, 130, 246, 0.75)", 'rgba(245, 158, 11, 0.75)', 'rgba(168, 85, 247, 0.75)'][i], width=2),
                    name=f'Média Móvel ({janela} dias)',
                    meta=janela,
                    customdata = df_historico[[f'ma{janela}']],
                    hovertemplate=
                    "<br><b>Média Móvel (%{meta} dias)</b><br>"
                    "$%{customdata[0]:,.2f}<br>" +
                    "<extra></extra>"
                )
            )
    
    fig.update_traces(
        hoverlabel=dict(
            bgcolor="black",
            font_size=14
        )
    )
    
    fig.update_layout(
        xaxis_title='Data',
        yaxis_title='Preço (USD)',
        xaxis_rangeslider_visible=False,
        paper_bgcolor="#111827",    
        plot_bgcolor="#111827",
        font=dict(
            family="Arial",
            size=14,
            color="white"
        ),
        hovermode="x unified",
        xaxis=dict(
        unifiedhovertitle=dict(
            text="<b>%{x|%d/%m/%Y %H:%M}</b>"
        )
    )
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255,255,255,0.10)',
        tickformat='%d/%m',
        showline=True,
        linewidth=1,
        linecolor='rgba(255,255,255,0.10)'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255,255,255,0.10)',
        showline=True,
        linewidth=1,
        linecolor='rgba(255,255,255,0.10)',
        tickprefix='$',
    )
    
    
    return fig