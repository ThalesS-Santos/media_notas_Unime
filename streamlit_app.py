import streamlit as st

# Configuração da página - Importante: layout wide ajuda no responsivo do Streamlit
st.set_page_config(page_title="Calculadora Medicina UNIME", page_icon="🩺", layout="wide")

# CSS Focado em Responsividade (Mobile First)
st.markdown("""
<style>
    /* Esto geral para evitar overflow lateral no celular */
    .main .block-container {
        padding: 1rem 1rem;
        max-width: 100%;
    }

    /* Títulos que diminuem no celular */
    .main-title {
        font-size: clamp(1.5rem, 5vw, 2.5rem);
        text-align: center;
        color: #1e293b;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    /* Placar que vira lista no celular */
    .stat-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        margin-bottom: 20px;
    }

    .stat-box {
        flex: 1 1 150px; /* Garante que o box quebre linha se não couber */
        background: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }

    .stat-box h2 {
        font-size: 1.8rem !important;
        margin: 0;
    }

    /* Card de Input otimizado */
    .input-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 12px;
        width: 100%;
    }

    .input-label {
        font-weight: 700;
        font-size: 1rem;
        color: #334155;
        display: block;
        margin-bottom: 5px;
    }

    .input-sub {
        font-size: 0.8rem;
        color: #64748b;
        margin-bottom: 10px;
    }

    /* Ajuste para os inputs do Streamlit não ficarem gigantes */
    .stTextInput > div > div > input {
        height: 45px;
        font-size: 16px !important; /* Evita zoom automático no iOS */
    }

    /* Card de Meta/Alvo */
    .target-card {
        background: #f1f5f9;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #2e5a88;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho adaptável
st.markdown('<h1 class="main-title">🩺 Notas Medicina UNIME</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 25px;'>Média mínima obrigatória: <b>7.0</b></p>", unsafe_allow_html=True)

# Dados do Sistema UNIME
pesos = {
    "PBL (5 etapas)": 2.0,
    "TBL - gRAT (Grupo)": 1.0,
    "TBL - iRAT (Individual)": 1.5,
    "Prova Teórica": 3.4,
    "Lab. Práticas Integradas": 0.7,
    "Lab. Morfofuncional": 1.4
}

# Lógica de cálculo
notas_digitadas = {}
notas_finais = {}

# --- ÁREA DE INPUTS (Empilhada no Mobile) ---
# Usamos colunas, mas o Streamlit as empilha automaticamente em telas pequenas
cols = st.columns([1, 1])

for i, (nome, peso_max) in enumerate(pesos.items()):
    with cols[i % 2]:
        st.markdown(f"""
        <div class="input-card">
            <span class="input-label">{nome}</span>
            <div class="input-sub">Peso: {peso_max} pts no total</div>
        """, unsafe_allow_html=True)
        
        nota_val = st.text_input(f"Nota {nome}", key=f"in_{nome}", label_visibility="collapsed", placeholder="Sua nota (0-10)")
        
        if nota_val:
            try:
                n = float(nota_val.replace(',', '.'))
                if 0 <= n <= 10:
                    notas_digitadas[nome] = n
                    notas_finais[nome] = (n / 10) * peso_max
                else: st.error("Use 0 a 10")
            except: st.error("Número inválido")
        st.markdown("</div>", unsafe_allow_html=True)

# --- CÁLCULOS ---
nota_atual = sum(notas_finais.values())
media_alvo = 7.0
faltam_para_7 = max(0.0, media_alvo - nota_atual)
pontos_em_aberto = sum([peso for nome, peso in pesos.items() if nome not in notas_digitadas])

# --- PLACAR DE RESULTADOS (Responsivo) ---
st.markdown('<div class="stat-container">', unsafe_allow_html=True)

# Card 1: Acumulado
st.markdown(f"""<div class="stat-box"><small>ACUMULADO</small><h2 style="color:#2e5a88;">{nota_atual:.2f}</h2></div>""", unsafe_allow_html=True)

# Card 2: Falta
if nota_atual < media_alvo:
    st.markdown(f"""<div class="stat-box"><small>FALTA PARA 7</small><h2 style="color:#e11d48;">{faltam_para_7:.2f}</h2></div>""", unsafe_allow_html=True)
else:
    st.markdown(f"""<div class="stat-box" style="border-color:#22c55e;"><small>STATUS</small><h2 style="color:#22c55e;">PASSOU!</h2></div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- SEÇÃO DE PREDIÇÃO (O QUE FALTA) ---
if 0 < pontos_em_aberto < 10 and nota_atual < media_alvo:
    aproveitamento = (faltam_para_7 / pontos_em_aberto)
    nota_alvo_10 = aproveitamento * 10
    
    st.markdown('<div class="target-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Meta para as próximas")
    
    if nota_alvo_10 > 10:
        st.error(f"Mesmo tirando 10 em tudo que falta, você somaria {nota_atual + pontos_em_aberto:.2f}. Atenção ao Exame Final.")
    else:
        st.write(f"Para fechar com **7.0**, você precisa de uma média **{nota_alvo_10:.2f}** nas notas que faltam.")
        st.progress(min(nota_alvo_10/10, 1.0))
    st.markdown('</div>', unsafe_allow_html=True)

if nota_atual >= media_alvo:
    st.balloons()

st.markdown("<br><p style='text-align: center; color: #94a3b8; font-size: 0.8rem;'>Feito para a melhor estudante de medicina da UNIME ❤️</p>", unsafe_allow_html=True)
