import streamlit as st

dashboard = st.Page(
    "pages/Dashboard.py",
    title="Dashboard",
    icon=":material/dashboard:"
)

market_explorer = st.Page(
    "pages/Market Explorer.py",
    title="Market Explorer",
    icon=":material/search:",
)

pg = st.navigation([
    dashboard,
    market_explorer
],
    position='hidden'
)

with st.sidebar:
    st.image('assets/images/cripto2.webp', width=200)
    
    st.divider()
    
    st.page_link(
        dashboard,
        label="Dashboard",
        icon=":material/dashboard:"
    )

    st.page_link(
        market_explorer,
        label="Market Explorer",
        icon=":material/search:"
    )
    
pg.run()