import streamlit as st
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Tibia Bank Manager 2026", layout="wide")

# --- INICIALIZAÇÃO DO ESTADO ---
if 'saldo' not in st.session_state:
    st.session_state.saldo = 0
if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'itens_personalizados' not in st.session_state:
    st.session_state.itens_personalizados = ["Potion", "Imbuement", "Bless", "Ring/Collar", "Gold Token", "Transfer PT", "Loot"]

st.title("⚔️ Gestor Financeiro Tibia")

# --- SIDEBAR: GESTÃO DE SALDO ---
with st.sidebar:
    st.header("💰 Configurações de Saldo")
    saldo_manual = st.number_input("Definir Saldo Atual (GPS):", min_value=0, step=10000)
    if st.button("Atualizar Saldo Inicial"):
        st.session_state.saldo = saldo_manual
        st.session_state.historico.insert(0, f"{datetime.now().strftime('%H:%M')} | 🔵 Saldo ajustado para {saldo_manual:,d}")
        st.rerun()
    
    st.divider()
    if st.button("Resetar Tudo"):
        st.session_state.saldo = 0
        st.session_state.historico = []
        st.rerun()

# --- ÁREA PRINCIPAL ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Calculadora de Apoio (Pós-Hunt)")
    st.write("Use para descobrir o valor total antes de registrar.")
    c1, c2 = st.columns(2)
    with c1:
        s_antes = st.number_input("Saldo Antes:", min_value=0, step=1000, key="calc_antes")
    with c2:
        s_depois = st.number_input("Saldo Depois:", min_value=0, step=1000, key="calc_depois")
    
    resultado_hunt = s_depois - s_antes
    st.metric("Resultado da Hunt", f"{resultado_hunt:,d} GP")

    st.divider()
    
    st.subheader("📝 Registrar no Saldo Real")
    valor_mov = st.number_input("Valor da Operação (GPS):", min_value=0, step=1000, key="op_valor")
    tipo_item = st.selectbox("Categoria:", st.session_state.itens_personalizados)
    
    b1, b2 = st.columns(2)
    with b1:
        if st.button("➕ Somar ao Saldo", use_container_width=True):
            st.session_state.saldo += valor_mov
            st.session_state.historico.insert(0, f"{datetime.now().strftime('%H:%M')} | 🟢 +{valor_mov:,d} ({tipo_item})")
            st.rerun()
    with b2:
        if st.button("➖ Descontar do Saldo", use_container_width=True):
            st.session_state.saldo -= valor_mov
            st.session_state.historico.insert(0, f"{datetime.now().strftime('%H:%M')} | 🔴 -{valor_mov:,d} ({tipo_item})")
            st.rerun()

with col2:
    st.subheader("💰 Saldo no Jogo")
    # Estilo visual igual à imagem que você mandou
    valor_formatado = f"{int(st.session_state.saldo):,d}"
    st.markdown(f"""
        <div style="background-color: #1a1a1a; padding: 25px; border-radius: 10px; border: 2px solid #444;">
            <h1 style="text-align: center; color: #FFFFFF; font-family: monospace; margin: 0;">
                {valor_formatado} <span style="color: #FFD700;">●</span>
            </h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("### 📜 Histórico de Ações")
    if not st.session_state.historico:
        st.info("Nenhuma movimentação registrada.")
    for registro in st.session_state.historico[:12]:
        st.write(registro)

st.divider()
st.caption("Controle Manual Tibia 2026 | Matheus - Rio Grande do Sul")
