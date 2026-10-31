import pandas as pd
import numpy as np

from processing.history_processing import processar_historico
from processing.market_processing import processar_dados_mercado
from utils.formatting import formatar_numero

def gerar_diagnostico_mercado():
    pass

def analisar_tendencia(df_historico):
    ultimo = df_historico.iloc[-1]

    if ultimo["price"] > ultimo["ma7"] > ultimo["ma30"] > ultimo["ma90"]:
        return "Forte Alta"

    elif ultimo["price"] > ultimo["ma30"] > ultimo["ma90"]:
        return "Alta"

    elif ultimo["price"] < ultimo["ma7"] < ultimo["ma30"] < ultimo["ma90"]:
        return "Forte Baixa"

    elif ultimo["price"] < ultimo["ma30"] < ultimo["ma90"]:
        return "Baixa"

    return "Consolidação"

    
    