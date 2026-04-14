import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

st.set_page_config(page_title="Frasco de Areia - Ambiental Metrosul", layout="centered")

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

# --- FUNÇÃO PARA GERAR PDF (VERSÃO SEM FOTO) ---
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "RELATÓRIO DE ENSAIO - FRASCO DE AREIA", ln=True, align='C')
    pdf.set_font("Arial", "I", 9)
    pdf.cell(200, 5, "Norma DNER-ME 092/94 - Determinação da Massa Específica 'in situ'", ln=True, align='C')
    pdf.ln(5)

    # 1. IDENTIFICAÇÃO
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(190, 7, " 1. IDENTIFICAÇÃO", border=1, ln=True, fill=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(95, 8, f" OS: {dados['os']}", border=1)
    pdf.cell(95, 8, f" Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}", border=1, ln=True)
    pdf.multi_cell(190, 8, f" Local: {dados['endereco']}", border=1)
    pdf.ln(3)

    # 2. UMIDADE
    pdf.set_font("Arial", "B", 10)
    pdf.cell(190, 7, " 2. DETERMINAÇÃO DA UMIDADE", border=1, ln=True, fill=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(63, 8, f" Solo Úmido+B: {dados['p_bu']:.1f}g", border=1)
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
    pdf.cell(95, 8, f" Peso Solo Úmido Cava: {dados['p_solo_real']:.1f}g", border=1)
    pdf.cell(95, 8, f" Volume da Cava: {dados['vol']:.1f} cm3", border=1, ln=True)
    pdf.ln(3)

    # 4. CONCLUSÃO
    pdf.set_font("Arial", "B", 10)
    pdf.cell(190, 7, " 4. CONCLUSÃO", border=1, ln=True, fill=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(95, 8, " Densidade Seca de Campo:", border=1); pdf.cell(95, 8, f" {dados['dens_seca']:.3f} g/cm3", border=1, ln=True)
    pdf.cell(95, 8, f" Proctor Máximo (Lab):", border=1); pdf.cell(95, 8, f" {dados['proctor']:.3f} g/cm3", border=1, ln=True)
    
    pdf.ln(5)
    if dados['gc'] >= dados['limite']:
        pdf.set_text_color(0, 100, 0)
        txt_status = f"APROVADO (Min: {dados['limite']}%)"
    else:
        pdf.set_text_color(200, 0, 0)
        txt_status = f"RECOMPACTAR (Min: {dados['limite']}%)"
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 15, f" GRAU DE COMPACTAÇÃO: {dados['gc']:.1f} %", border=1, ln=True, align='C')
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, txt_status, border=0, ln=True, align='C')

    return pdf.output(dest='S').encode('latin-1')

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Configurações Fixas")
    d_areia = st.number_input("Densidade Areia (g/cm³)", value=st.session_state.configs_frasco["dens_areia"], format="%.3f", step=0.001)
    p_cone = st.number_input("Peso no Cone (g)", value=st.session_state.configs_frasco["peso_cone"], format="%.1f")
    p_max = st.number_input("Proctor Máximo (g/cm³)", value=st.session_state.configs_frasco["proctor_max"], format="%.3f", step=0.001)
    
    st.subheader("Taras e Limites")
    t_umid = st.number_input("Peso Bandeja Umid. (g)", value=st.session_state.configs_frasco["tara_bandeja_umid"])
    t_cava = st.number_input("Peso Bandeja Cava (g)", value=st.session_state.configs_frasco["tara_bandeja_cava"])
    limite = st.selectbox("Mínimo Exigido (G.C.)", [95.0, 100.0])

    if st.button("💾 Salvar Configurações", use_container_width=True):
        st.session_state.configs_frasco = {
            "dens_areia": d_areia, "peso_cone": p_cone, "proctor_max": p_max,
            "tara_bandeja_umid": t_umid, "tara_bandeja_cava": t_cava, "limite_gc": limite
        }
        st.success("Salvo!")

# --- INTERFACE PRINCIPAL ---
st.title("🧪 Frasco de Areia in Situ")

st.header("1. Identificação")
num_os = st.text_input("Número da OS")
endereco = st.text_area("Local do Ensaio")

st.header("2. Determinação da Umidade")
c1, c2 = st.columns(2)
with c1: p_bu_raw = st.number_input("Bandeja + Solo Úmido", format="%.3f", step=0.001)
with c2: p_bs_raw = st.number_input("Bandeja + Solo Seco", format="%.3f", step=0.001)

p_bu = ajustar_peso(p_bu_raw)
p_bs = ajustar_peso(p_bs_raw)
tara_u = st.session_state.configs_frasco["tara_bandeja_umid"]
umid = ((p_bu - p_bs) / (p_bs - tara_u)) * 100 if (p_bs - tara_u) > 0 else 0.0
st.info(f"Umidade: {umid:.2f} %")

st.header("3. Peso do Solo da Cava")
p_st_raw = st.number_input("Total (Solo Úmido + Bandeja)", format="%.3f", step=0.001)
p_st = ajustar_peso(p_st_raw)
peso_solo_real = p_st - st.session_state.configs_frasco["tara_bandeja_cava"]

st.header("4. Frasco com Areia")
f1, f2 = st.columns(2)
with f1: p_i_raw = st.number_input("Peso Inicial do Frasco", format="%.3f", step=0.001)
with f2: p_f_raw = st.number_input("Peso Final do Frasco", format="%.3f", step=0.001)

p_ini = ajustar_peso(p_i_raw)
p_fin = ajustar_peso(p_f_raw)

# CÁLCULOS FINAIS
if p_ini > 0 and peso_solo_real > 0:
    p_areia_cava = p_ini - p_fin - st.session_state.configs_frasco["peso_cone"]
    vol = p_areia_cava / st.session_state.configs_frasco["dens_areia"]
    d_umida = peso_solo_real / vol
    d_seca = d_umida / (1 + (umid / 100))
    gc = (d_seca / st.session_state.configs_frasco["proctor_max"]) * 100
    
    limite_atual = st.session_state.configs_frasco["limite_gc"]
    status = "APROVADO" if gc >= limite_atual else "RECOMPACTAR"

    st.divider()
    res1, res2 = st.columns(2)
    res1.metric("Densidade Seca", f"{d_seca:.3f} g/cm³")
    res2.metric("G.C. (%)", f"{gc:.1f}%")

    dados_pdf = {
        "os": num_os, "endereco": endereco, "umidade": umid,
        "p_bu": p_bu, "p_bs": p_bs, "tara_u": tara_u,
        "p_ini": p_ini, "p_fin": p_fin, "p_cone": st.session_state.configs_frasco["peso_cone"],
        "p_areia_cava": p_areia_cava, "p_solo_real": peso_solo_real, "vol": vol,
        "dens_seca": d_seca, "proctor": st.session_state.configs_frasco["proctor_max"],
        "gc": gc, "status": status, "limite": limite_atual
    }
    
    pdf_bytes = gerar_pdf(dados_pdf)
    st.download_button("📥 Baixar PDF", pdf_bytes, f"Ensaio_{num_os}.pdf", "application/pdf", use_container_width=True)
