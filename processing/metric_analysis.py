import pandas as pd
from utils.fonts import carregar_fontes

ANALISE_VOLUME_RELATIVO = {
    "Muito Alto": {
        "icon": ":material/arrow_outward:",
        "color": "green",
        "background": "green",
        "label": "Muito Alto"
    },
    "Alto": {
        "icon": ":material/arrow_outward:",
        "color": "green",
        "background": "green",
        "label": "Alto"
    },
    "Normal": {
        "icon": ":material/check_indeterminate_small:",
        "color": "yellow",
        "background": "yellow",
        "label": "Normal"
    },
    "Baixo": {
        "icon": ":material/arrow_downward:",
        "color": "orange",
        "background": "orange",
        "label": "Baixo"
    },
    "Muito Baixo": {
        "icon": ":material/arrow_downward:",
        "color": "red",
        "background": "red",
        "label": "Muito Baixo"
    }
}


def analisar_volume_relativo(delta):
    if delta >= 30:
        return ANALISE_VOLUME_RELATIVO["Muito Alto"]

    if delta >= 10:
        return ANALISE_VOLUME_RELATIVO["Alto"]

    if delta >= -10:
        return ANALISE_VOLUME_RELATIVO["Normal"]

    if delta >= -30:
        return ANALISE_VOLUME_RELATIVO["Baixo"]

    return ANALISE_VOLUME_RELATIVO["Muito Baixo"]

ANALISE_MA = {
    "Muito Acima": {
        "icon": ":material/arrow_outward:",
        "color": "green",
        "background": "green",
        "label": "Muito Acima"
    },
    "Acima": {
        "icon": ":material/arrow_outward:",
        "color": "green",
        "background": "green",
        "label": "Acima"
    },
    "Neutra": {
        "icon": ":material/check_indeterminate_small:",
        "color": "yellow",
        "background": "yellow",
        "label": "Neutra"
    },
    "Abaixo": {
        "icon": ":material/arrow_downward:",
        "color": "orange",
        "background": "orange",
        "label": "Abaixo"
    },
    "Muito Abaixo": {
        "icon": ":material/arrow_downward:",
        "color": "red",
        "background": "red",
        "label": "Muito Abaixo"
    }
}


def analisar_ma(delta):
    if delta >= 2:
        return ANALISE_MA["Muito Acima"]

    if delta >= 0.5:
        return ANALISE_MA["Acima"]

    if delta >= -0.5:
        return ANALISE_MA["Neutra"]

    if delta >= -2:
        return ANALISE_MA["Abaixo"]

    return ANALISE_MA["Muito Abaixo"]

ANALISE_ATH = {
    "Muito Próximo": {
        "icon": ":material/arrow_outward:",
        "color": "green",
        "background": "green",
        "label": "Muito Próximo"
    },
    "Próximo": {
        "icon": ":material/arrow_outward:",
        "color": "green",
        "background": "green",
        "label": "Próximo"
    },
    "Correção": {
        "icon": ":material/check_indeterminate_small:",
        "color": "yellow",
        "background": "yellow",
        "label": "Correção"
    },
    "Muito Distante": {
        "icon": ":material/arrow_downward:",
        "color": "red",
        "background": "red",
        "label": "Muito Distante"
    }
}


def analisar_ath(delta):
    if delta >= 3:
        return ANALISE_ATH["Muito Próximo"]

    if delta >= 1:
        return ANALISE_ATH["Próximo"]

    if delta >= -1:
        return ANALISE_ATH["Correção"]

    return ANALISE_ATH["Muito Distante"]

ANALISE_DRAWDOWN = {
    "Leve": {
        "icon": ":material/arrow_outward:",
        "color": "green",
        "background": "green",
        "label": "Correção Leve"
    },
    "Moderado": {
        "icon": ":material/check_indeterminate_small:",
        "color": "yellow",
        "background": "yellow",
        "label": "Correção"
    },
    "Forte": {
        "icon": ":material/arrow_downward:",
        "color": "orange",
        "background": "orange",
        "label": "Queda Forte"
    },
    "Severo": {
        "icon": ":material/arrow_downward:",
        "color": "red",
        "background": "red",
        "label": "Bear Market"
    }
}


def analisar_drawdown(delta):
    if delta >= 3:
        return ANALISE_DRAWDOWN["Leve"]

    if delta >= 1:
        return ANALISE_DRAWDOWN["Moderado"]

    if delta >= -1:
        return ANALISE_DRAWDOWN["Forte"]

    return ANALISE_DRAWDOWN["Severo"]

ANALISE_VOLATILIDADE = {
    "Baixa": {
        "icon": ":material/arrow_outward:",
        "color": "green",
        "background": "green",
        "label": "Baixa"
    },
    "Moderada": {
        "icon": ":material/check_indeterminate_small:",
        "color": "yellow",
        "background": "yellow",
        "label": "Moderada"
    },
    "Alta": {
        "icon": ":material/arrow_downward:",
        "color": "orange",
        "background": "orange",
        "label": "Alta"
    },
    "Extrema": {
        "icon": ":material/arrow_downward:",
        "color": "red",
        "background": "red",
        "label": "Extrema"
    }
}


def analisar_volatilidade(delta):
    if delta <= -1:
        return ANALISE_VOLATILIDADE["Baixa"]

    if delta <= 0.3:
        return ANALISE_VOLATILIDADE["Moderada"]

    if delta <= 1:
        return ANALISE_VOLATILIDADE["Alta"]

    return ANALISE_VOLATILIDADE["Extrema"]

ANALISE_RETORNO = {
    "Alta Forte": {
        "icon": ":material/arrow_outward:",
        "color": "green",
        "background": "green",
        "label": "Alta Forte"
    },
    "Alta": {
        "icon": ":material/arrow_outward:",
        "color": "green",
        "background": "green",
        "label": "Alta"
    },
    "Estável": {
        "icon": ":material/check_indeterminate_small:",
        "color": "yellow",
        "background": "yellow",
        "label": "Estável"
    },
    "Queda": {
        "icon": ":material/arrow_downward:",
        "color": "orange",
        "background": "orange",
        "label": "Queda"
    },
    "Queda Forte": {
        "icon": ":material/arrow_downward:",
        "color": "red",
        "background": "red",
        "label": "Queda Forte"
    }
}


def analisar_retorno(retorno):
    if retorno >= 5:
        return ANALISE_RETORNO["Alta Forte"]

    if retorno >= 2:
        return ANALISE_RETORNO["Alta"]

    if retorno >= -2:
        return ANALISE_RETORNO["Estável"]

    if retorno >= -5:
        return ANALISE_RETORNO["Queda"]

    return ANALISE_RETORNO["Queda Forte"]

ANALISE_MARKET_CAP = {
    "Big Cap": {
        "icon": ":material/arrow_outward:",
        "color": "green",
        "background": "green",
        "label": "Big Cap"
    },
    "Mid Cap": {
        "icon": ":material/check_indeterminate_small:",
        "color": "yellow",
        "background": "yellow",
        "label": "Mid Cap"
    },
    "Small Cap": {
        "icon": ":material/arrow_downward:",
        "color": "red",
        "background": "red",
        "label": "Small Cap"
    }
}


def analisar_market_cap(categoria):
    return ANALISE_MARKET_CAP[categoria]

def analisar_retorno_acumulado(retorno):
    if retorno >= 100:
        return ANALISE_RETORNO_ACUMULADO["Muito Positivo"]

    if retorno >= 20:
        return ANALISE_RETORNO_ACUMULADO["Positivo"]

    if retorno >= -20:
        return ANALISE_RETORNO_ACUMULADO["Neutro"]

    if retorno >= -50:
        return ANALISE_RETORNO_ACUMULADO["Negativo"]

    return ANALISE_RETORNO_ACUMULADO["Muito Negativo"]