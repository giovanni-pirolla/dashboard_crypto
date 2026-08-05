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
        "icon": ":material/call_received:",
        "color": "orange",
        "background": "orange",
        "label": "Baixo"
    },
    "Muito Baixo": {
        "icon": ":material/call_received:",
        "color": "red",
        "background": "red",
        "label": "Muito Baixo"
    }
}


def analisar_volume_relativo(volume_relativo):
    if volume_relativo >= 2:
        return ANALISE_VOLUME_RELATIVO["Muito Alto"]

    if volume_relativo >= 1.3:
        return ANALISE_VOLUME_RELATIVO["Alto"]

    if volume_relativo >= 0.8:
        return ANALISE_VOLUME_RELATIVO["Normal"]

    if volume_relativo >= 0.5:
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
        "icon": ":material/call_received:",
        "color": "orange",
        "background": "orange",
        "label": "Abaixo"
    },
    "Muito Abaixo": {
        "icon": ":material/call_received:",
        "color": "red",
        "background": "red",
        "label": "Muito Abaixo"
    }
}


def analisar_ma(distancia):
    if distancia >= 10:
        return ANALISE_MA["Muito Acima"]

    if distancia >= 3:
        return ANALISE_MA["Acima"]

    if distancia >= -3:
        return ANALISE_MA["Neutra"]

    if distancia >= -10:
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
        "icon": ":material/call_received:",
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

ANALISE_DELTA = {
    "Aumento": {
        "icon": ":material/arrow_outward:",
        "color": "green",
        "background": "green",
    },
    "Queda": {
        "icon": ":material/call_received:",
        "color": "red",
        "background": "red",
    }
}


def analisar_delta(delta):
    if delta >= 0:
        return ANALISE_DELTA["Aumento"]
    
    if delta < 0:
        return ANALISE_DELTA["Queda"]

    return ANALISE_DELTA["Aumento"]


ANALISE_MARKET_CAP = {
    "Big Cap": {
        "icon": ":material/account_balance:",
        "color": "green",
        "background": "green",
        "label": "Big Cap"
    },
    "Mid Cap": {
        "icon": ":material/account_balance:",
        "color": "yellow",
        "background": "yellow",
        "label": "Mid Cap"
    },
    "Small Cap": {
        "icon": ":material/account_balance:",
        "color": "red",
        "background": "red",
        "label": "Small Cap"
    }
}


def analisar_market_cap(categoria):
    return ANALISE_MARKET_CAP[categoria]

