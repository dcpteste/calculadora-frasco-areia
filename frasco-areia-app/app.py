import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Tibia Daily Manager 2026", layout="wide")

# --- INICIALIZAÇÃO DO ESTADO ---
if 'saldo' not in st.session_state:
    st.session_state.saldo = 0.0
if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'log_diario' not in st.session_state:
    st.session_state.log_diario = []
if 'itens_personalizados' not in st.session_state:
    st.session_state.itens_personalizados = ["Potion", "Imbuement", "Bless", "Ring/Collar", "Premium", "Gold Token"]

st.title("⚔️ Gestor Tibia: Fechamento Diário")

# --- SIDEBAR ---
with st.sidebar:
    st.header("💰 Saldo Inicial")
    saldo_manual = st.number_input("Quanto você tem agora? (GPS):", min_value=0.0, step=10000.0)
    if st.button("Definir Saldo"):
        st.session_state.saldo = saldo_manual
        st.rerun()

    st.divider()
    st.header("⚙️ Configurações")
    novo_item = st.text_input("Novo item de gasto:")
    if st.button("Cadastrar Item"):
        if novo_item and novo_item not in st.session_state.itens_personalizados:
            st.session_state.itens_personalizados.append(novo_item)
            st.rerun()

# --- ÁREA DE LANÇAMENTO ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Registrar Movimentação")
    valor_mov = st.number_input("Valor (GPS):", min_value=0.0, step=1000.0, key="mov")
    tipo_item = st.selectbox("Categoria:", st.session_state.itens_personalizados + ["Loot (Soma)"])
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➖ Descontar", use_container_width=True):
            st.session_state.saldo -= valor_mov
            st.session_state.historico.insert(0, f"{datetime.now().strftime('%H:%M')} | 🔴 -{valor_mov:,.0f} ({tipo_item})")
            st.rerun()
    with c2:
        if st.button("➕ Somar", use_container_width=True):
            st.session_state.saldo += valor_mov
            st.session_state.historico.insert(0, f"{datetime.now().strftime('%H:%M')} | 🟢 +{valor_mov:,.0f} (Loot)")
            st.rerun()

    st.divider()
    # BOTÃO DE FECHAMENTO
    if st.button("📅 FINALIZAR DIA JOGADO", type="primary", use_container_width=True):
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        resumo = f"📅 {data_hoje} | Saldo Final: {st.session_state.saldo:,.0f} GP"
        st.session_state.log_diario.insert(0, resumo)
        st.balloons() # Efeito visual de comemoração
        st.success(f"Dia {data_hoje} finalizado com sucesso!")

with col2:
    st.subheader("Saldo Atual")
    cor_saldo = "green" if st.session_state.saldo >= 0 else "red"
    st.markdown(f"<h1 style='text-align: center; color: {cor_saldo};'>{st.session_state.saldo:,.0f} GP</h1>".replace(",", "."), unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Histórico da Sessão", "Resumo por Dia"])
    
    with tab1:
        for registro in st.session_state.historico[:10]:
            st.write(registro)
            
    with tab2:
        for dia in st.session_state.log_diario:
            st.info(dia)

# Exportação (Geralmente útil para o seu estudo de Power BI depois)
if st.session_state.log_diario:
    st.download_button("Baixar Relatório de Dias", 
                       data="\n".join(st.session_state.log_diario), 
                       file_name="fechamento_tibia_2026.txt")
