import streamlit as st

st.set_page_config(page_title="Tibia Hunt Analyzer 2026", page_icon="⚔️")

st.title("⚔️ Calculadora de Hunt - Tibia")

with st.sidebar:
    st.header("Configurações de Custo")
    # Preços médios dos itens de Imbuement (Market)
    preco_token = st.number_input("Preço Gold Token", value=50000)
    taxa_imbue = 250000 # Taxa fixa do Powerful
    
    st.info("Dica: 1h de hunt consome 1/20 do valor total do Imbuement.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Dados da Hunt")
    tempo = st.slider("Duração da Hunt (minutos)", 30, 180, 60)
    loot = st.number_input("Loot Total (GPS)", min_value=0, step=1000)
    supplies = st.number_input("Gastos com Potes/Runas (GPS)", min_value=0, step=1000)

# Cálculo automático (Assumindo 3 slots de Imbuement Powerful)
# Se cada slot custa ~2kk (itens + taxa), total 6kk por 20h
custo_hora_imbue = (3 * (2000000)) / 20 
custo_proporcional_imbue = (custo_hora_imbue / 60) * tempo

total_gastos = supplies + custo_proporcional_imbue
lucro_final = loot - total_gastos

with col2:
    st.subheader("Resultado Real")
    st.metric("Lucro Final", f"{lucro_final:,.0f} gp".replace(",", "."), 
              delta=f"{(lucro_final/tempo)*60:,.0f} gp/h".replace(",", "."))
    
    st.write(f"**Custo Invisível (Imbuements):** {custo_proporcional_imbue:,.0f} gp".replace(",", "."))

if lucro_final > 0:
    st.success("Hunt Lucrativa! 💰")
elif lucro_final < 0:
    st.error("Hunt no Prejuízo! 📉")

st.divider()
st.caption("Desenvolvido para organizar os gastos de EK e Monk em 2026.")
