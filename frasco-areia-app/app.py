import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

st.set_page_config(page_title="Frasco de Areia | Ambiental Metrosul", page_icon="🧪", layout="centered")

# --- ESTILO CUSTOMIZADO (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE AJUSTE AUTOMÁTICO ---
def ajustar_peso(valor):
    if 0 < valor < 20:
        return valor * 1000
    return valor

# --- MEMÓRIA E CONFIGURAÇÕES ---
if 'configs_frasco' not in st.session_state:
    st.session_state.configs_frasco = {
        "dens_areia": 1.450,
        "peso_cone": 1540.0,
        "proctor_max": 2.050,
        "tara_bandeja_umid": 100.0,
        "tara_bandeja_cava": 500.0,
        "limite_gc": 95.0
    }

# --- FUNÇÃO PARA GERAR PDF ---
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "RELATÓRIO DE ENSAIO - FRASCO DE AREIA", ln=True, align='C')
    pdf.set_font("Arial", "I", 9)
    pdf.cell(200, 5, "Norma DNER-ME 092/94", ln=True, align='C')
    pdf.ln(5)

    sections = [
        ("1. IDENTIFICAÇÃO", [f"OS: {dados['os']}", f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}", f"Local: {dados['endereco']}"]),
        ("2. UMIDADE", [f"Solo Úmido+B: {dados['p_bu']:.1f}g", f"Solo Seco+B: {dados['p_bs']:.1f}g", f"Tara Bandeja: {dados['tara_u']:.1f}g", f"UMIDADE: {dados['umidade']:.2f} %"]),
        ("3. PESOS E VOLUMES", [f"Inic. Frasco: {dados['p_ini']:.1f}g", f"Final Frasco: {dados['p_fin']:.1f}g", f"Areia Cava: {dados['p_areia_cava']:.1f}g", f"Volume Cava: {dados['vol']:.1f} cm3"]),
        ("4. CONCLUSÃO", [f"Dens. Seca: {dados['dens_seca']:.3f} g/cm3", f"Proctor Lab: {dados['proctor']:.3f} g/cm3"])
    ]

    for title, lines in sections:
        pdf.set_fill_color(230, 230, 230)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(190, 7, f" {title}", border=1, ln=True, fill=True)
        pdf.set_font("Arial", "", 10)
        for line in lines:
            pdf.cell(190, 8, f" {line}", border=1, ln=True)
        pdf.ln(2)

    pdf.ln(5)
    color = (0, 100, 0) if dados['gc'] >= dados['limite'] else (200, 0, 0)
    pdf.set_text_color(*color)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 15, f" GRAU DE COMPACTAÇÃO: {dados['gc']:.1f} %", border=1, ln=True, align='C')
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, f"STATUS: {dados['status']}", border=0, ln=True, align='C')
    return pdf.output(dest='S').encode('latin-1')

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Painel de Controle")
    with st.expander("Calibração do Frasco", expanded=False):
        d_areia = st.number_input("Dens. Areia (g/cm³)", value=st.session_state.configs_frasco["dens_areia"], format="%.3f")
        p_cone = st.number_input("Peso no Cone (g)", value=st.session_state.configs_frasco["peso_cone"])
        p_max = st.number_input("Proctor Máximo (g/cm³)", value=st.session_state.configs_frasco["proctor_max"], format="%.3f")
    
    with st.expander("Taras e Normas", expanded=False):
        t_umid = st.number_input("Bandeja Umidade (g)", value=st.session_state.configs_frasco["tara_bandeja_umid"])
        t_cava = st.number_input("Bandeja Cava (g)", value=st.session_state.configs_frasco["tara_bandeja_cava"])
        limite = st.selectbox("G.C. Mínimo", [95.0, 100.0])

    if st.button("💾 Salvar Configurações", use_container_width=True):
        st.session_state.configs_frasco.update({"dens_areia": d_areia, "peso_cone": p_cone, "proctor_max": p_max, "tara_bandeja_umid": t_umid, "tara_bandeja_cava": t_cava, "limite_gc": limite})
        st.success("Configurações atualizadas!")

# --- APP PRINCIPAL ---
st.title("🏗️ Ensaio de Frasco de Areia")
st.caption("Controle de Compactação de Solo - Engenharia de Campo")

with st.container():
    st.subheader("📋 1. Identificação")
    c1, c2 = st.columns(2)
    num_os = c1.text_input("Número da OS", placeholder="Ex: 2024-001")
    endereco = c2.text_input("Local/Estaca", placeholder="Ex: Rua X, Km 12")

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🔥 2. Umidade")
    p_bu_raw = st.number_input("Bandeja + Solo Úmido", format="%.3f", step=0.001)
    p_bs_raw = st.number_input("Bandeja + Solo Seco", format="%.3f", step=0.001)
    p_bu, p_bs = ajustar_peso(p_bu_raw), ajustar_peso(p_bs_raw)
    t_u = st.session_state.configs_frasco["tara_bandeja_umid"]
    umid = ((p_bu - p_bs) / (p_bs - t_u)) * 100 if (p_bs - t_u) > 0 else 0.0
    st.info(f"**Umidade:** {umid:.2f}%")

with col_b:
    st.subheader("🕳️ 3. Solo da Cava")
    p_st_raw = st.number_input("Total (Solo + Bandeja)", format="%.3f", step=0.001)
    p_st = ajustar_peso(p_st_raw)
    peso_solo = p_st - st.session_state.configs_frasco["tara_bandeja_cava"]
    st.info(f"**Solo Líquido:** {peso_solo:.1f}g")

st.divider()

st.subheader("⚖️ 4. Pesagem do Frasco")
f1, f2 = st.columns(2)
p_i_raw = f1.number_input("Peso Inicial do Frasco", format="%.3f", step=0.001)
p_f_raw = f2.number_input("Peso Final do Frasco", format="%.3f", step=0.001)
p_ini, p_fin = ajustar_peso(p_i_raw), ajustar_peso(p_f_raw)

# --- RESULTADOS ---
if p_ini > 0 and peso_solo > 0:
    p_areia_cava = p_ini - p_fin - st.session_state.configs_frasco["peso_cone"]
    vol = p_areia_cava / st.session_state.configs_frasco["dens_areia"]
    d_seca = (peso_solo / vol) / (1 + (umid / 100)) if vol > 0 else 0
    gc = (d_seca / st.session_state.configs_frasco["proctor_max"]) * 100
    
    lim = st.session_state.configs_frasco["limite_gc"]
    status = "APROVADO ✅" if gc >= lim else "RECOMPACTAR ⚠️"
    
    st.markdown(f"### Resultado Final: **{status}**")
    r1, r2, r3 = st.columns(3)
    r1.metric("Densidade Seca", f"{d_seca:.3f}")
    r2.metric("G.C. (%)", f"{gc:.1f}%")
    r3.metric("Meta Min.", f"{lim}%")

    dados_pdf = {"os": num_os, "endereco": endereco, "umidade": umid, "p_bu": p_bu, "p_bs": p_bs, "tara_u": t_u, "p_ini": p_ini, "p_fin": p_fin, "p_cone": st.session_state.configs_frasco["peso_cone"], "p_areia_cava": p_areia_cava, "p_solo_real": peso_solo, "vol": vol, "dens_seca": d_seca, "proctor": st.session_state.configs_frasco["proctor_max"], "gc": gc, "status": status, "limite": lim}
    
    pdf_bytes = gerar_pdf(dados_pdf)
    st.download_button("📩 Baixar Relatório Técnico", pdf_bytes, f"Ensaio_{num_os}.pdf", "application/pdf", use_container_width=True)
