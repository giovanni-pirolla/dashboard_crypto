import pandas as pd

ANALISE_VOLUME_RELATIVO = {
    "Muito Alto": {
        "icon": "🟢",
        "color": "#22c55e",
        "background": "#14532d",
        "label": "Muito Alto"
    },
    "Alto": {
        "icon": "🟢",
        "color": "#4ade80",
        "background": "#166534",
        "label": "Alto"
    },
    "Normal": {
        "icon": "🟡",
        "color": "#facc15",
        "background": "#713f12",
        "label": "Normal"
    },
    "Baixo": {
        "icon": "🟠",
        "color": "#fb923c",
        "background": "#7c2d12",
        "label": "Baixo"
    },
    "Muito Baixo": {
        "icon": "🔴",
        "color": "#ef4444",
        "background": "#7f1d1d",
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
        "icon": "🚀",
        "color": "#16a34a",
        "background": "#14532d",
        "label": "Muito Acima"
    },
    "Acima": {
        "icon": "🟢",
        "color": "#22c55e",
        "background": "#166534",
        "label": "Acima"
    },
    "Neutra": {
        "icon": "🟡",
        "color": "#eab308",
        "background": "#713f12",
        "label": "Neutra"
    },
    "Abaixo": {
        "icon": "🟠",
        "color": "#fb923c",
        "background": "#7c2d12",
        "label": "Abaixo"
    },
    "Muito Abaixo": {
        "icon": "🔴",
        "color": "#ef4444",
        "background": "#7f1d1d",
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
        "icon": "🏆",
        "color": "#22c55e",
        "background": "#14532d",
        "label": "Muito Próximo"
    },
    "Próximo": {
        "icon": "🟢",
        "color": "#4ade80",
        "background": "#166534",
        "label": "Próximo"
    },
    "Correção": {
        "icon": "🟡",
        "color": "#facc15",
        "background": "#713f12",
        "label": "Correção"
    },
    "Muito Distante": {
        "icon": "🔴",
        "color": "#ef4444",
        "background": "#7f1d1d",
        "label": "Muito Distante"
    }
}


def analisar_ath(distancia):
    distancia = abs(distancia)

    if distancia <= 10:
        return ANALISE_ATH["Muito Próximo"]

    if distancia <= 30:
        return ANALISE_ATH["Próximo"]

    if distancia <= 60:
        return ANALISE_ATH["Correção"]

    return ANALISE_ATH["Muito Distante"]

ANALISE_DRAWDOWN = {
    "Leve": {
        "icon": "🟢",
        "color": "#22c55e",
        "background": "#14532d",
        "label": "Correção Leve"
    },
    "Moderado": {
        "icon": "🟡",
        "color": "#eab308",
        "background": "#713f12",
        "label": "Correção"
    },
    "Forte": {
        "icon": "🟠",
        "color": "#fb923c",
        "background": "#7c2d12",
        "label": "Queda Forte"
    },
    "Severo": {
        "icon": "🔴",
        "color": "#ef4444",
        "background": "#7f1d1d",
        "label": "Bear Market"
    }
}


def analisar_drawdown(drawdown):
    drawdown = abs(drawdown)

    if drawdown <= 10:
        return ANALISE_DRAWDOWN["Leve"]

    if drawdown <= 30:
        return ANALISE_DRAWDOWN["Moderado"]

    if drawdown <= 50:
        return ANALISE_DRAWDOWN["Forte"]

    return ANALISE_DRAWDOWN["Severo"]

ANALISE_VOLATILIDADE = {
    "Baixa": {
        "icon": "🟢",
        "color": "#22c55e",
        "background": "#14532d",
        "label": "Baixa"
    },
    "Moderada": {
        "icon": "🟡",
        "color": "#facc15",
        "background": "#713f12",
        "label": "Moderada"
    },
    "Alta": {
        "icon": "🟠",
        "color": "#fb923c",
        "background": "#7c2d12",
        "label": "Alta"
    },
    "Extrema": {
        "icon": "🔴",
        "color": "#ef4444",
        "background": "#7f1d1d",
        "label": "Extrema"
    }
}


def analisar_volatilidade(volatilidade):
    if volatilidade <= 2:
        return ANALISE_VOLATILIDADE["Baixa"]

    if volatilidade <= 5:
        return ANALISE_VOLATILIDADE["Moderada"]

    if volatilidade <= 8:
        return ANALISE_VOLATILIDADE["Alta"]

    return ANALISE_VOLATILIDADE["Extrema"]

ANALISE_RETORNO = {
    "Alta Forte": {
        "icon": "🚀",
        "color": "#16a34a",
        "background": "#14532d",
        "label": "Alta Forte"
    },
    "Alta": {
        "icon": "🟢",
        "color": "#22c55e",
        "background": "#166534",
        "label": "Alta"
    },
    "Estável": {
        "icon": "🟡",
        "color": "#facc15",
        "background": "#713f12",
        "label": "Estável"
    },
    "Queda": {
        "icon": "🟠",
        "color": "#fb923c",
        "background": "#7c2d12",
        "label": "Queda"
    },
    "Queda Forte": {
        "icon": "🔴",
        "color": "#ef4444",
        "background": "#7f1d1d",
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
        "icon": "🏦",
        "color": "#3b82f6",
        "background": "#1e3a8a",
        "label": "Big Cap"
    },
    "Mid Cap": {
        "icon": "🏢",
        "color": "#8b5cf6",
        "background": "#4c1d95",
        "label": "Mid Cap"
    },
    "Small Cap": {
        "icon": "🏪",
        "color": "#f97316",
        "background": "#7c2d12",
        "label": "Small Cap"
    }
}


def analisar_market_cap(categoria):
    return ANALISE_MARKET_CAP[categoria]