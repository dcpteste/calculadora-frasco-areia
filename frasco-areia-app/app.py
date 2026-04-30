import streamlit as st
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Tibia Financeiro 2026", layout="wide")

# --- INICIALIZAÇÃO DO ESTADO (Saldo começa zerado) ---
if 'saldo' not in st.session_state:
    st.session_state.saldo = 0
if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'log_diario' not in st.session_state:
    st.session_state.log_diario = []
if 'itens_personalizados' not in st.session_state:
    st.session_state.itens_personalizados = ["Potion", "Imbuement", "Bless", "Ring/Collar", "Premium", "Gold Token"]

st.title("⚔️ Gestor de GPS - Tibia")

# --- SIDEBAR: CONFIGURAÇÕES E SALDO INICIAL ---
with st.sidebar:
    st.header("💰 Gestão de Saldo")
    # Permite que você adicione o saldo que tem agora no jogo
    saldo_inicial = st.number_input("Definir Saldo Atual (GPS):", min_value=0, step=10000)
    if st.button("Atualizar Saldo Principal"):
        st.session_state.saldo = saldo_inicial
        st.session_state.historico.insert(0, f"{datetime.now().strftime('%H:%M')} | 🔵 Saldo definido para {saldo_inicial:,d}")
        st.rerun()

    st.divider()
    st.header("⚙️ Cadastro de Itens")
    novo_item = st.text_input("Novo tipo de gasto:")
    if st.button("Adicionar à Lista"):
        if novo_item and novo_item not in st.session_state.itens_personalizados:
            st.session_state.itens_personalizados.append(novo_item)
            st.rerun()

    if st.button("Resetar Tudo (Zerar)"):
        st.session_state.saldo = 0
        st.session_state.historico = []
        st.session_state.log_diario = []
        st.rerun()

# --- ÁREA PRINCIPAL ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Registrar Movimentação")
    
    valor_mov = st.number_input("Valor da Operação:", min_value=0, step=1000)
    tipo_item = st.selectbox("Categoria:", st.session_state.itens_personalizados + ["Loot (Soma)"])
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➖ Descontar Gasto", use_container_width=True):
            st.session_state.saldo -= valor_mov
            st.session_state.historico.insert(0, f"{datetime.now().strftime('%H:%M')} | 🔴 -{valor_mov:,d} ({tipo_item})")
            st.rerun()
    
    with c2:
        if st.button("➕ Somar Loot", use_container_width=True):
            st.session_state.saldo += valor_mov
            st.session_state.historico.insert(0, f"{datetime.now().strftime('%H:%M')} | 🟢 +{valor_mov:,d} (Loot)")
            st.rerun()

    st.divider()
    if st.button("📅 FINALIZAR DIA JOGADO", type="primary", use_container_width=True):
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        resumo = f"📅 {data_hoje} | Saldo Final: {st.session_state.saldo:,d} GP"
        st.session_state.log_diario.insert(0, resumo)
        st.balloons()
        st.success(f"Resumo de {data_hoje} salvo!")

with col2:
    st.subheader("Saldo no Jogo (Estilo Tibia)")
    
    # Formatação igual à imagem enviada: Fundo escuro e vírgulas nos milhares
    valor_formatado = f"{int(st.session_state.saldo):,d}"
    st.markdown(f"""
        <div style="background-color: #1a1a1a; padding: 20px; border-radius: 10px; border: 2px solid #444; margin-bottom: 20px;">
            <h1 style="text-align: center; color: #FFFFFF; font-family: 'Courier New', Courier, monospace; margin: 0;">
                {valor_formatado} <span style="color: #FFD700;">●</span>
            </h1>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Histórico da Sessão", "Fechamentos Diários"])
    
    with tab1:
        if not st.session_state.historico:
            st.write("Nenhuma movimentação hoje.")
        for registro in st.session_state.historico[:15]:
            st.write(registro)
            
    with tab2:
        if not st.session_state.log_diario:
            st.write("Nenhum dia finalizado ainda.")
        for dia in st.session_state.log_diario:
            st.info(dia)

st.divider()
st.caption(f"Controle Financeiro Tibia 2026 | Usuário: Matheus | Local: Gravataí-RS")
