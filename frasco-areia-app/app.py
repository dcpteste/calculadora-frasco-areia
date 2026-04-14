import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

st.set_page_config(page_title="Frasco de Areia | Ambiental Metrosul", page_icon="🧪", layout="centered")

# --- FUNÇÃO DE AJUSTE AUTOMÁTICO (KG para G) ---
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

# --- FUNÇÃO PARA GERAR PDF (FORMATO DETALHADO E SEGURO) ---
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "RELATORIO DE ENSAIO - FRASCO DE AREIA", ln=True, align='C')
    pdf.set_font("Arial", "I", 9)
    pdf.cell(200, 5, "Norma DNER-ME 092/94 - Ensaio de Campo", ln=True, align='C')
    pdf.ln(5)

    # 1. IDENTIFICAÇÃO
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(190, 7, " 1. IDENTIFICACAO", border=1, ln=True, fill=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(95, 8, f" OS: {dados['os']}", border=1)
    pdf.cell(95, 8, f" Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}", border=1, ln=True)
    pdf.multi_cell(190, 8, f" Local: {dados['endereco']}", border=1)
    pdf.ln(3)

    # 2. UMIDADE
    pdf.set_font("Arial", "B", 10)
    pdf.cell(190, 7, " 2. DETERMINACAO DA UMIDADE", border=1, ln=True, fill=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(63, 8, f" Solo Umido+B: {dados['p_bu']:.1f}g", border=1)
    pdf.cell(63, 8, f" Solo Seco+B: {dados['p_bs']:.1f}g", border=1)
    pdf.cell(64, 8, f" Tara Bandeja: {dados['tara_u']:.1f}g", border=1, ln=True)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(190, 8, f" UMIDADE (%) : {dados['umidade']:.2f} %", border=1, ln=True, align='R')
    pdf.ln(3)

    # 3. PESOS E VOLUMES
    pdf.set_font("Arial", "B", 10)
    pdf.cell(190, 7, " 3. PESOS E VOLUMES", border=1, ln=True, fill=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(95, 8, f" Peso Inicial Frasco: {dados['p_ini']:.1f}g", border=1)
    pdf.cell(95, 8, f" Peso Final Frasco: {dados['p_fin']:.1f}g", border=1, ln=True)
    pdf.cell(95, 8, f" Peso Areia no Cone: {dados['p_cone']:.1f}g", border=1)
    pdf.cell(95, 8, f" Peso Areia na Cava: {dados['p_areia_cava']:.1f}g", border=1, ln=True)
    pdf.cell(95, 8, f" Peso Solo Umido Cava: {dados['p_solo_real']:.1f}g", border=1)
    pdf.cell(95, 8, f" Volume da Cava: {dados['vol']:.1f} cm3", border=1, ln=True)
    pdf.ln(3)

    # 4. CONCLUSÃO
    pdf.set_font("Arial", "B", 10)
    pdf.cell(190, 7, " 4. CONCLUSAO", border=1, ln=True, fill=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(95, 8, " Densidade Seca de Campo:", border=1); pdf.cell(95, 8, f" {dados['dens_seca']:.3f} g/cm3", border=1, ln=True)
    pdf.cell(95, 8, f" Proctor Maximo (Lab):", border=1); pdf.cell(95, 8, f" {dados['proctor']:.3f} g/cm3", border=1, ln=True)
    
    pdf.ln(5)
    color = (0, 100, 0) if dados['gc'] >= dados['limite'] else (200, 0, 0)
    pdf.set_text_color(*color)
    
    status_simples = "APROVADO" if dados['gc'] >= dados['limite'] else "RECOMPACTAR"
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 15, f" GRAU DE COMPACTACAO: {dados['gc']:.1f} %", border=1, ln=True, align='C')
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, f"STATUS: {status_simples} (Minimo: {dados['limite']}%)", border=0, ln=True, align='C')

    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Configurações")
    d_areia = st.number_input("Dens. Areia (g/cm³)", value=st.session_state.configs_frasco["dens_areia"], format="%.3f")
    p_cone = st.number_input("Peso no Cone (g)", value=st.session_state.configs_frasco["peso_cone"])
    p_max = st.number_input("Proctor Máximo (g/cm³)", value=st.session_state.configs_frasco["proctor_max"], format="%.3f")
    t_umid = st.number_input("Bandeja Umidade (g)", value=st.session_state.configs_frasco["tara_bandeja_umid"])
    t_cava = st.number_input("Bandeja Cava (g)", value=st.session_state.configs_frasco["tara_bandeja_cava"])
    limite = st.selectbox("G.C. Mínimo", [95.0, 100.0])

    if st.button("💾 Salvar Dados", use_container_width=True):
        st.session_state.configs_frasco.update({"dens_areia": d_areia, "peso_cone": p_cone, "proctor_max": p_max, "tara_bandeja_umid": t_umid, "tara_bande_cava": t_cava, "limite_gc": limite})
        st.success("Configurações salvas!")

# --- INTERFACE PRINCIPAL ---
st.title("🏗️ Frasco de Areia")

st.subheader
