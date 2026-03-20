import streamlit as st

# Configuração da página - Tema Clean e Ícone
st.set_page_config(page_title="Dashboard Acadêmico Medicina", page_icon="🩺", layout="wide")

# ==========================================
# INJEÇÃO DE CSS PERSONALIZADO (A MÁGICA VISUAL)
# ==========================================
st.markdown("""
<style>
    /* Fundo Principal Clean */
    .stApp {
        background-color: #f8fafc;
    }

    /* Estilo para Títulos Principais */
    .big-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        font-size: 2.8rem;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        color: #64748b;
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* ESTILO DOS CARTÕES DE NOTA (INPUT CARDS) */
    .note-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
        transition: transform 0.2s;
    }
    .note-card:hover {
        transform: translateY(-2px);
    }
    .card-title {
        font-weight: 700;
        color: #334155;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    .card-info {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }

    /* Input Style Reset (para os inputs ficarem cleans nos cards) */
    div.stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #f8fafc !important;
    }

    /* ESTILO DO CARD DE RESULTADO PRINCIPAL */
    .result-card {
        background-color: #ffffff;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 10px 15px rgba(0,0,0,0.05);
        border: 2px solid #2e5a88;
        margin-bottom: 1.5rem;
    }
    .result-card h1 {
        color: #2e5a88 !important;
        font-weight: 900 !important;
        font-size: 4rem !important;
        margin: 0 !important;
    }
    .result-card-subtitle {
        color: #64748b;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.1rem;
        font-size: 0.9rem;
    }

    /* Estilo para Mensagens de Status na Coluna 2 */
    .status-area {
        margin-top: 1rem;
        padding: 1.5rem;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# ESTRUTURA DO DASHBOARD
# ==========================================

# CABEÇALHO PRINCIPAL
st.markdown('<h1 class="big-title">Dashboard de Metas: UNIME</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Acompanhe seu progresso e planeje seu semestre.</p>', unsafe_allow_html=True)


# BARRA LATERAL (SIDEBAR)
with st.sidebar:
    st.image("https://raw.githubusercontent.com/fboldt/unime_medicine_grades/main/unime_logo_full.png", width=150) # Tente colocar o link da logo da UNIME aqui
    st.markdown("## Instruções 🎓")
    st.write("Doutora, digite sua nota de **0 a 10** em cada campo. O sistema faz a somatória automática ponderada.")
    
    st.divider()
    
    # Configuração da Média
    media_aprovacao = st.number_input("Nota mínima para passar:", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
    
    st.divider()
    st.info("💡 Este site não salva seus dados. É necessário redigitar as notas a cada acesso.")


# PESOS OFICIAIS (Da foto dela)
pesos = {
    "PBL (5 etapas)": 2.0,
    "TBL - gRAT (Grupo)": 1.0,
    "TBL - iRAT (Individual)": 1.5,
    "Prova Teórica": 3.4,
    "Lab. Práticas Integradas": 0.7,
    "Lab. Morfofuncional": 1.4
}

# Dicionários para armazenar valores
notas_digitadas = {}
notas_finais = {}

# COLUNAGEM PRINCIPAL
col1, col2 = st.columns([1.8, 1])


# COLUNA 1: ENTRADA DE NOTAS (DESIGN DE CARDS)
with col1:
    st.markdown("### 📝 Suas Avaliações")
    
    for nome, peso_max in pesos.items():
        # Criação do Card Visual para cada nota
        st.markdown(f"""
        <div class="note-card">
            <div class="card-title">{nome}</div>
            <p class="card-info">Sua nota de 0 a 10 nesta categoria.</p>
        """, unsafe_allow_html=True)
        
        # Colocamos o Input e a mini barra de progresso do peso dentro do card
        nota_c1, nota_c2 = st.columns([2, 1])
        
        with nota_c1:
            nota_input = st.text_input(f"Nota para {nome}", value="", key=f"p_{nome}", label_visibility="collapsed")
            
            # Validação e Cálculo
            if nota_input:
                try:
                    valor = float(nota_input.replace(',', '.'))
                    if 0 <= valor <= 10:
                        notas_digitadas[nome] = valor
                        # Cálculo da regra de três: (nota/10) * peso_max
                        notas_finais[nome] = (valor / 10) * peso_max
                    else:
                        st.error(f"Nota deve ser entre 0 e 10.")
                except ValueError:
                    st.error(f"Formato inválido.")
        
        with nota_c2:
            st.write("") # Espaçador
            st.write(f"Soma **+{peso_max:.1f}pts** no total")
            # Uma mini barra que mostra o "rendimento" da nota inserida (em %)
            if nome in notas_digitadas:
                rendimento_parcial = notas_digitadas[nome] / 10.0
                st.progress(rendimento_parcial, text=f"Rend. {rendimento_parcial*100:.0f}%")
        
        st.markdown("</div>", unsafe_allow_html=True) # Fecha o div do card


# COLUNA 2: RESULTADOS (VISUALIZAÇÃO DE IMPACTO)
with col2:
    st.markdown("### 📊 Status Atual")
    
    nota_total = sum(notas_finais.values())
    pontos_preenchidos = sum([pesos[k] for k in notas_finais.keys()])
    pontos_faltantes = 10.0 - pontos_preenchidos
    
    # --- CARD DE RESULTADO PRINCIPAL ---
    st.markdown(f"""
        <div class="result-card">
            <p class="result-card-subtitle">Sua Pontuação Acumulada</p>
            <h1>{nota_total:.2f} <span style='font-size: 2rem; color: #cbd5e1;'>/ 10.0</span></h1>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    
    # Barra de Progresso Geral
    percentual_media = min(nota_total / media_aprovacao, 1.0) if media_aprovacao > 0 else 0
    # Muda a cor da barra dependendo se passou ou não
    cor_barra = "green" if nota_total >= media_aprovacao else "orange" if pontos_faltantes > 0 else "red"
    st.progress(percentual_media, text=f"Progresso até a meta ({nota_total:.2f}/{media_aprovacao:.1f})")

    st.write("")

    # --- LÓGICA DE STATUS ---
    st.divider()
    
    # Se ela preencheu pelo menos uma nota
    if pontos_preenchidos > 0:
        
        # STATUS 1: JÁ PASSOU
        if nota_total >= media_aprovacao:
            st.success(f"🏆 PARABÉNS! Você já atingiu a média necessária ({media_aprovacao}).")
            st.balloons()
            st.info("Você pode usar os campos vazios para prever com quanto vai fechar o semestre!")
        
        # STATUS 2: AINDA FALTA
        elif pontos_faltantes > 0:
            falta_para_passar = media_aprovacao - nota_total
            
            # Verificamos se ainda é matematicamente possível passar
            if falta_para_passar > pontos_faltantes:
                st.error(f"⚠️ Alerta Crítico: Situação Matemática Difícil.")
                st.write(f"Restam apenas **{pontos_faltantes:.2f} pts** a serem conquistados, mas você precisa de **{falta_para_passar:.2f} pts** para a média. Procure seu professor sobre o exame final.")
            
            else:
                # Cálculo do rendimento necessário
                # Isso calcula qual % de acerto ela precisa ter no que resta
                percentual_necessario = (falta_para_passar / pontos_faltantes) * 100
                rendimento_nota = (percentual_necessario / 10.0) # Converte % de acerto em nota de 0-10
                
                st.warning(f"Faltam **{falta_para_passar:.2f} pontos** para atingir a média.")
                st.write(f"Você precisa de um rendimento médio de **{percentual_necessario:.1f}% (nota {rendimento_nota:.1f})** no restante das avaliações.")
                
                # Feedback motivacional
                if rendimento_nota > 8.5:
                    st.info("Rendimento necessário alto. Hora de focar nos estudos da Prova Teórica!")
                elif rendimento_nota > 7.0:
                    st.info("Situação sob controle. Mantenha a consistência!")
                else:
                    st.info("Situação tranquila. Você está perto da meta!")
                    
    # STATUS 3: TELA VAZIA
    else:
        st.info("👋 Aguardando o preenchimento da primeira nota para calcular as projeções.")
