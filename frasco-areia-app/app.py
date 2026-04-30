import streamlit as st
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Tibia Bank Manager 2026", layout="wide")

# --- INICIALIZAÇÃO DO ESTADO ---
if 'saldo' not in st.session_state:
    st.session_state.saldo = 0
if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'log_diario' not in st.session_state:
    st.session_state.log_diario = []
if 'itens_personalizados' not in st.session_state:
    st.session_state.itens_personalizados = ["Potion", "Imbuement", "Bless", "Ring/Collar", "Gold Token", "Transfer PT", "Loot"]

st.title("⚔️ Gestor Financeiro Tibia")

# --- SIDEBAR ---
with st.sidebar:
    st.header("💰 Configurações")
    saldo_manual = st.number_input("Definir Saldo Atual (GPS):", min_value=0, step=10000)
    if st.button("Atualizar Saldo Inicial"):
        st.session_state.saldo = saldo_manual
        st.session_state.historico.insert(0, f"{datetime.now().strftime('%H:%M')} | 🔵 Saldo ajustado para {saldo_manual:,d}")
        st.rerun()
    
    st.divider()
    if st.button("Resetar Tudo"):
        st.session_state.saldo = 0
        st.session_state.historico = []
        st.session_state.log_diario = []
        st.rerun()

# --- ÁREA PRINCIPAL ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Calculadora de Apoio")
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

    st.write("---")
    # BOTÃO DE FINALIZAR O DIA (VOLTOU!)
    if st.button("📅 FINALIZAR DIA JOGADO", type="primary", use_container_width=True):
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        resumo = f"📅 {data_hoje} | Saldo Final: {int(st.session_state.saldo):,d} GP"
        st.session_state.log_diario.insert(0, resumo)
        st.balloons()
        st.success(f"Fechamento de {data_hoje} realizado!")

with col2:
    st.subheader("💰 Saldo no Jogo")
    valor_formatado = f"{int(st.session_state.saldo):,d}"
    st.markdown(f"""
        <div style="background-color: #1a1a1a; padding: 25px; border-radius: 10px; border: 2px solid #444;">
            <h1 style="text-align: center; color: #FFFFFF; font-family: monospace; margin: 0;">
                {valor_formatado} <span style="color: #FFD700;">●</span>
            </h1>
        </div>
    """, unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Histórico de Hoje", "Resumo de Dias Anteriores"])
    with t1:
        for registro in st.session_state.historico[:15]:
            st.write(registro)
    with t2:
        for dia in st.session_state.log_diario:
            st.info(dia)

st.divider()
st.caption("Gestor Tibia 2026 | Matheus - RS")
