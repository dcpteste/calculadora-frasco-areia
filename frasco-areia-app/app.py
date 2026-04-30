import streamlit as st

st.set_page_config(page_title="Tibia Bank Manager 2026", layout="wide")

# --- INICIALIZAÇÃO DO ESTADO ---
if 'saldo' not in st.session_state:
    st.session_state.saldo = 0.0
if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'itens_personalizados' not in st.session_state:
    st.session_state.itens_personalizados = ["Potion", "Imbuement", "Bless", "Ring/Collar", "Premium", "Gold Token"]

st.title("⚖️ Gestor Financeiro Tibia")

# --- SIDEBAR: GESTÃO DE ITENS E SALDO INICIAL ---
with st.sidebar:
    st.header("💰 Configurar Saldo")
    # Campo para definir o saldo atual manualmente
    saldo_manual = st.number_input("Definir Saldo Atual (GPS):", min_value=0.0, step=10000.0, format="%.0f")
    if st.button("Atualizar Saldo Inicial"):
        st.session_state.saldo = saldo_manual
        st.session_state.historico.insert(0, f"🔵 Saldo ajustado manualmente para {saldo_manual:,.0f}")
        st.success("Saldo atualizado!")
        st.rerun()

    st.divider()
    st.header("⚙️ Itens de Gasto")
    novo_item = st.text_input("Cadastrar novo tipo de item:")
    if st.button("Adicionar Item à Lista"):
        if novo_item and novo_item not in st.session_state.itens_personalizados:
            st.session_state.itens_personalizados.append(novo_item)
            st.success(f"{novo_item} adicionado!")

    if st.button("Resetar Tudo"):
        st.session_state.saldo = 0
        st.session_state.historico = []
        st.rerun()

# --- ÁREA PRINCIPAL: ENTRADA E SAÍDA ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Registrar Movimentação")
    
    valor_mov = st.number_input("Valor da Operação (GPS):", min_value=0.0, step=1000.0, format="%.0f")
    tipo_item = st.selectbox("Categoria:", st.session_state.itens_personalizados + ["Loot (Soma)"])
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➖ Descontar Gasto", use_container_width=True):
            st.session_state.saldo -= valor_mov
            st.session_state.historico.insert(0, f"🔴 -{valor_mov:,.0f} ({tipo_item})")
            st.rerun()
    
    with c2:
        if st.button("➕ Somar Entrada", use_container_width=True):
            st.session_state.saldo += valor_mov
            st.session_state.historico.insert(0, f"🟢 +{valor_mov:,.0f} (Loot/Entrada)")
            st.rerun()

with col2:
    st.subheader("Saldo em Tempo Real")
    # Formatação visual
    cor_saldo = "green" if st.session_state.saldo >= 0 else "red"
    # Substituindo vírgula por ponto para o padrão brasileiro de visualização se desejar
    valor_formatado = f"{st.session_state.saldo:,.0f}".replace(",", ".")
    st.markdown(f"<h1 style='text-align: center; color: {cor_saldo};'>{valor_formatado} GP</h1>", unsafe_allow_html=True)
    
    st.write("**Histórico Recente:**")
    for registro in st.session_state.historico[:8]: # Mostra os últimos 8
        st.write(registro)

# --- BOTÃO PARA SALVAR ---
st.divider()
if st.button("📥 Salvar Histórico em TXT"):
    with open("historico_hunt.txt", "w", encoding="utf-8") as f:
        f.write(f"Saldo Final: {st.session_state.saldo}\n")
        f.write("-" * 30 + "\n")
        for h in st.session_state.historico:
            f.write(h + "\n")
    st.download_button("Clique aqui para baixar o arquivo", 
                       data="\n".join(st.session_state.historico), 
                       file_name="historico_tibia.txt")
