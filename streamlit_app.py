import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora Medicina UNIME", page_icon="🩺", layout="wide")

# CSS para um visual moderno e sem sidebar
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    
    /* Remove margens extras do topo */
    .main .block-container { padding-top: 2rem; }

    .main-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
    }

    .stat-box {
        background: #f1f5f9;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #cbd5e1;
    }

    .input-card {
        background: #ffffff;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 10px;
    }

    .target-text {
        color: #0f172a;
        font-weight: 700;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown("<h1 style='text-align: center; color: #1e293b;'>🩺 Calculadora de Notas Medicina</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Sistema Somativo UNIME - Média para Aprovação: <b>7.0</b></p>", unsafe_allow_html=True)

# Pesos Oficiais
pesos = {
    "PBL (5 etapas)": 2.0,
    "TBL - gRAT (Grupo)": 1.0,
    "TBL - iRAT (Individual)": 1.5,
    "Prova Teórica": 3.4,
    "Lab. Práticas Integradas": 0.7,
    "Lab. Morfofuncional": 1.4
}

# Inicialização de variáveis
notas_digitadas = {}
notas_finais = {}
media_alvo = 7.0

# --- ÁREA DE RESULTADO (PLACAR) ---
col_score1, col_score2, col_score3 = st.columns([1, 1, 1])

placeholder_nota = col_score1.empty()
placeholder_falta = col_score2.empty()
placeholder_status = col_score3.empty()

st.divider()

# --- ÁREA DE INPUT ---
st.markdown("### 📝 Suas Notas (0 a 10)")
cols_input = st.columns(2)

# Distribuindo os inputs em duas colunas para facilitar a leitura
for i, (nome, peso_max) in enumerate(pesos.items()):
    with cols_input[i % 2]:
        st.markdown(f"""<div class="input-card"><b>{nome}</b> <br><small>Peso máximo no semestre: {peso_max} pts</small>""", unsafe_allow_html=True)
        nota_val = st.text_input(f"Nota {nome}", value="", key=f"input_{nome}", label_visibility="collapsed", placeholder="Digite de 0 a 10...")
        
        if nota_val:
            try:
                n = float(nota_val.replace(',', '.'))
                if 0 <= n <= 10:
                    notas_digitadas[nome] = n
                    notas_finais[nome] = (n / 10) * peso_max
                else:
                    st.error("Nota entre 0 e 10!")
            except:
                st.error("Número inválido")
        st.markdown("</div>", unsafe_allow_html=True)

# --- CÁLCULOS E PREVISÕES ---
nota_atual = sum(notas_finais.values())
pontos_em_aberto = sum([peso for nome, peso in pesos.items() if nome not in notas_digitadas])
faltam_para_7 = max(0.0, media_alvo - nota_atual)

# Atualizando Placar Superior
placeholder_nota.markdown(f"""<div class="stat-box"><small>PONTOS ACUMULADOS</small><br><h2 style='color:#2e5a88; margin:0;'>{nota_atual:.2f}</h2></div>""", unsafe_allow_html=True)
placeholder_falta.markdown(f"""<div class="stat-box"><small>FALTA PARA O 7.0</small><br><h2 style='color:#e11d48; margin:0;'>{faltam_para_7:.2f}</h2></div>""", unsafe_allow_html=True)

if nota_atual >= media_alvo:
    placeholder_status.markdown(f"""<div class="stat-box" style="background:#dcfce7; border-color:#86efac;"><small>STATUS</small><br><h2 style='color:#166534; margin:0;'>APROVADA! 🎉</h2></div>""", unsafe_allow_html=True)
    st.balloons()
elif pontos_em_aberto == 0:
    placeholder_status.markdown(f"""<div class="stat-box" style="background:#fee2e2; border-color:#fca5a5;"><small>STATUS</small><br><h2 style='color:#991b1b; margin:0;'>EXAME FINAL</h2></div>""", unsafe_allow_html=True)
else:
    placeholder_status.markdown(f"""<div class="stat-box"><small>STATUS</small><br><h2 style='color:#1e293b; margin:0;'>EM CURSO</h2></div>""", unsafe_allow_html=True)

# --- SEÇÃO DE PREDIÇÃO AUTOMÁTICA ---
if 0 < pontos_em_aberto < 10:
    st.markdown("---")
    st.markdown("### 🎯 O que você precisa para passar?")
    
    # Se ainda faltam pontos para o 7
    if faltam_para_7 > 0:
        aproveitamento_necessario = (faltam_para_7 / pontos_em_aberto)
        nota_necessaria_0_10 = aproveitamento_necessario * 10
        
        if nota_necessaria_0_10 > 10:
            st.error(f"⚠️ Situação Crítica: Mesmo gabaritando o que resta, você somaria {nota_atual + pontos_em_aberto:.2f}. Será necessário exame final.")
        else:
            col_target1, col_target2 = st.columns([1, 2])
            with col_target1:
                st.metric("Nota Alvo (0 a 10)", f"{nota_necessaria_0_10:.2f}")
            with col_target2:
                st.write("")
                st.markdown(f"Para passar com 7.0, você precisa tirar uma média de **{nota_necessaria_0_10:.2f}** em **todas** as avaliações que ainda não preencheu.")
                st.progress(nota_necessaria_0_10 / 10)
    else:
        st.success("Você já atingiu os 7 pontos! Qualquer nota nas próximas provas apenas aumentará sua média final.")

st.markdown("<br><br><p style='text-align: center; color: #94a3b8; font-size: 0.8rem;'>Desenvolvido com ❤️ para a futura Dra.</p>", unsafe_allow_html=True)
