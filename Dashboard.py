import pandas as pd

# Existem mais de 5000 moedas registradas na API do coingecko, por esse motivo, optei por trabalhar apenas com as 12 mais conhecidas
# para evitar qualquer tipo de problema de performance ou desempenho do sistema pelo excesso de registros. Além disso, a versão gratuita da
# API do coingecko permite apenas um número limitado de requisições por minuto, o que impossibilita mais moedas exibidas ao mesmo tempo do 
# que essas
principais_moedas = {
    "bitcoin": "Bitcoin",
    "ethereum": "Ethereum",
    "solana": "Solana",
    "binancecoin": "BNB",
    "cardano": "Cardano"
}

# preco_inicial = df_historico['price'].iloc[0]
#     preco_atual = df_historico['price'].iloc[-1]
#     retorno_acumulado = ((preco_atual - preco_inicial) / preco_inicial) * 100