import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

st.set_page_config(page_title="Calibração de Areia - Metrosul", page_icon="⚖️", layout="centered")

# --- FUNÇÃO DE AJUSTE AUTOMÁTICO (KG para G) ---
def ajustar_peso(valor):
    if 0 < valor < 30:
        return valor * 1000
    return valor

# --- FUNÇÃO PARA GERAR PDF (PADRÃO TÉCNICO A-E) ---
def gerar_pdf_calib(dados):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "CALIBRACAO DA MASSA ESPECIFICA DA AREIA", ln=True, align='C')
    pdf.set_font("Arial", "I", 9)
    pdf.cell(200, 5, "Laboratorio de Solos - Ambiental Metrosul", ln=True, align='C')
    pdf.ln(10)

    # Tabela com o Passo a Passo
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(140, 8, " DESCRICAO DO CALCULO", border=1, fill=True)
    pdf.cell(50, 8, " RESULTADO", border=1, ln=True, fill=True, align='C')

    pdf.set_font("Arial", "", 10)
    
    # Linha A
    pdf.cell(140, 10, " A - Volume do Recipiente (cm3):", border=1)
    pdf.cell(50, 10, f"{dados['vol']:.1f}", border=1, ln=True, align='C')
    
    # Linha B
    pdf.cell(140, 10, " B - Massa do Recipiente + Areia (g):", border=1)
    pdf.cell(50, 10, f"{dados['p_total']:.1f}", border=1, ln=True, align='C')
    
    # Linha C
    pdf.cell(140, 10, " C - Massa do Recipiente Vazio (g):", border=1)
    pdf.cell(50, 10, f"{dados['p_vazio']:.1f}", border=1, ln=True, align='C')
    
    # Linha D (Cálculo)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(140, 10, " D - Massa da Areia (B - C) (g):", border=1)
    pdf.cell(50, 10, f"{dados['massa_a']:.1f}", border=1, ln=True, align='C')
    
    pdf.ln(5)
    
    # Resultado Final (Linha E)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(140, 15, " E - DENSIDADE DA AREIA (D / A) (g/cm3):", border=1, fill=True)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(50, 15, f"{dados['densidade']:.3f}", border=1, ln=True, align='C', fill=True)

    pdf.ln(10)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(190, 5, f"Data da Calibracao: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='R')
    
    # O "ignore" evita erros de encoding com caracteres especiais
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- INTERFACE ---
st.title("⚖️ Calibração de Areia")
st.write("Determine a densidade da areia seguindo o passo a passo técnico.")

with st.container():
    st.subheader("📋 1. Dados do Recipiente")
    vol_recipiente = st.number_input("A - Volume do Recipiente (cm³)", value=2120.0, format="%.1f")
    p_vazio = st.number_input("C - Massa do Recipiente Vazio (g)", format="%.1f")

st.divider()

with st.container():
    st.subheader("⚖️ 2. Pesagem")
    p_total_raw = st.number_input("B - Massa do Recipiente + Areia (g)", format="%.1f")
    p_total = ajustar_peso(p_total_raw)

# --- CÁLCULOS ---
if p_total > p_vazio and vol_recipiente > 0:
    massa_areia = p_total - p_vazio
    densidade_final = massa_areia / vol_recipiente
    
    st.divider()
    st.subheader("📊 Resultado")
    
    col_res1, col_res2 = st.columns(2)
    col_res1.metric("Massa da Areia (D)", f"{massa_areia:.1f} g")
    col_res2.metric("DENSIDADE (E)", f"{densidade_final:.3f}")

    # Organizar dados para o PDF
    dados_cal = {
        "vol": vol_recipiente,
        "p_total": p_total,
        "p_vazio": p_vazio,
        "massa_a": massa_areia,
        "densidade": densidade_final
    }
    
    pdf_bytes = gerar_pdf_calib(dados_cal)
    
    st.download_button(
        label="📥 Baixar Certificado de Calibração",
        data=pdf_bytes,
        file_name=f"Calibracao_Areia_{datetime.now().strftime('%d%m%Y')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

st.sidebar.info("""
**Instruções de Cálculo:**
- **D = B - C** (Peso líquido da areia)
- **E = D / A** (Massa específica final)
""")
