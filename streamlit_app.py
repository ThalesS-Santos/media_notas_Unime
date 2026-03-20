import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora de Média Acadêmica", page_icon="🎓")

# Estilo customizado simples
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Calculadora de Média")
st.subheader("Organize suas notas e planeje seu semestre!")

# Sidebar para configurações
with st.sidebar:
    st.header("Configurações")
    media_aprovacao = st.number_input("Média para aprovação:", min_value=0.0, max_value=10.0, value=7.0, step=0.5)
    qtd_provas = st.number_input("Quantidade total de provas:", min_value=1, max_value=10, value=3)
    st.info("Dica: Você pode mudar a média necessária se sua faculdade exigir algo diferente de 7.0.")

st.divider()

# Entrada de notas
col1, col2 = st.columns([1, 1])

notas = []
notas_preenchidas = 0
soma_notas = 0.0

with col1:
    st.write("### Suas Notas")
    for i in range(int(qtd_provas)):
        nota = st.text_input(f"Nota da Prova {i+1}:", value="", key=f"p{i}")
        if nota != "":
            try:
                n = float(nota.replace(',', '.'))
                if 0 <= n <= 10:
                    notas.append(n)
                    notas_preenchidas += 1
                    soma_notas += n
                else:
                    st.warning(f"A nota da Prova {i+1} deve ser entre 0 e 10.")
            except ValueError:
                st.error(f"Por favor, insira um número válido na Prova {i+1}.")

# Cálculos e Lógica
media_atual = soma_notas / notas_preenchidas if notas_preenchidas > 0 else 0.0
provas_restantes = int(qtd_provas) - notas_preenchidas

with col2:
    st.write("### Resumo")
    
    if notas_preenchidas > 0:
        # Cor da métrica baseada na média
        status_cor = "normal" if media_atual >= media_aprovacao else "inverse"
        st.metric("Sua Média Atual", f"{media_atual:.2f}")
        
        progresso = min(media_atual / media_aprovacao, 1.0)
        st.progress(progresso)

        if media_atual >= media_aprovacao and provas_restantes == 0:
            st.success("🎉 Parabéns! Você já passou!")
        elif provas_restantes > 0:
            # Cálculo de quanto precisa nas próximas
            nota_total_necessaria = media_aprovacao * qtd_provas
            nota_faltante = nota_total_necessaria - soma_notas
            
            if nota_faltante <= 0:
                st.success("✅ Você já atingiu a pontuação necessária para passar! Só mantenha o ritmo.")
            else:
                media_necessaria_proximas = nota_faltante / provas_restantes
                
                if media_necessaria_proximas > 10:
                    st.error(f"Situação difícil: Você precisa de uma média de {media_necessaria_proximas:.2f} nas próximas {provas_restantes} provas para passar.")
                else:
                    st.warning(f"Faltam {nota_faltante:.2f} pontos no total.")
                    st.info(f"Você precisa tirar, em média, **{media_necessaria_proximas:.2f}** nas próximas {provas_restantes} prova(s).")
    else:
        st.info("Aguardando o preenchimento da primeira nota para calcular as projeções.")

# Rodapé ou Informação Extra
st.divider()
if notas_preenchidas == qtd_provas:
    if media_atual >= media_aprovacao:
        st.balloons()
