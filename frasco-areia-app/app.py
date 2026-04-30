import streamlit as st

st.set_page_config(page_title="Tibia Manager 2026", layout="wide")

# --- INICIALIZAÇÃO DO ESTADO (Para não perder os dados ao clicar) ---
if 'saldo' not in st.session_state:
    st.session_state.saldo = 0.0
if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'itens_personalizados' not in st.session_state:
    st.session_state.itens_personalizados = ["Potion", "Imbuement", "Bless", "Ring/Collar", "Premium", "Gold Token"]

st.title("⚖️ Gestor Financeiro Tibia")

# --- SIDEBAR: GESTÃO DE ITENS ---
with st.sidebar:
    st.header("⚙️ Configurações")
    novo_item = st.text_input("Cadastrar novo tipo de item:")
    if st.button("Adicionar Item à Lista"):
        if novo_item and novo_item not in st.session_state.itens_personalizados:
            st.session_state.itens_personalizados.append(novo_item)
            st.success(f"{novo_item} adicionado!")

    if st.button("Resetar Saldo"):
        st.session_state.saldo = 0
        st.session_state.historico = []
        st.rerun()

# --- ÁREA PRINCIPAL: ENTRADA E SAÍDA ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Registrar Movimentação")
    
    valor = st.number_input("Valor (GPS):", min_value=0, step=1000)
    tipo_item = st.selectbox("O que é isso?", st.session_state.itens_personalizados + ["Loot (Soma)"])
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➖ Descontar", use_container_width=True):
            st.session_state.saldo -= valor
            st.session_state.historico.insert(0, f"🔴 Descontou {valor:,.0f} de {tipo_item}")
            st.rerun()
    
    with c2:
        if st.button("➕ Somar Loot", use_container_width=True):
            st.session_state.saldo += valor
            st.session_state.historico.insert(0, f"🟢 Somou {valor:,.0f} de Loot")
            st.rerun()

with col2:
    st.subheader("Saldo Atual")
    # Formatação visual do saldo
    cor_saldo = "green" if st.session_state.saldo >= 0 else "red"
    st.markdown(f"<h1 style='text-align: center; color: {cor_saldo};'>{st.session_state.saldo:,.0f} GP</h1>".replace(",", "."), unsafe_allow_html=True)
    
    st.write("**Últimas Movimentações:**")
    for registro in st.session_state.historico[:5]: # Mostra os últimos 5
        st.write(registro)

st.divider()
st.caption("Controle de gastos para EK / Monk - Tibia 2026")
