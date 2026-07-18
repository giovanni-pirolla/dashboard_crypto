import pandas as pd
import plotly.graph_objects as go

def criar_grafico_candles(df_candles: pd.DataFrame, df_historico: pd.DataFrame):
    fig = go.Figure()
    
    fig.add_trace(
        go.Candlestick(
            x=df_candles['date'],
            open=df_candles['open'],
            high=df_candles['high'],
            low=df_candles['low'],
            close=df_candles['close'],
            increasing_line_color='green',
            decreasing_line_color='red'
        )
    )
    
    return fig