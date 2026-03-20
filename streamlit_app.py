import streamlit as st

st.set_page_config(page_title="Calculadora Medicina UNIME", page_icon="🩺")

# Estilo para parecer um dashboard médico/acadêmico
st.markdown("""
    <style>
    .stApp { background-color: #f0f4f8; }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2e5a88;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🩺 Calculadora de Notas - Medicina")
st.subheader("Sistema de Avaliação UNIME")

# Dicionário com os pesos conforme a foto
pesos = {
    "PBL (5 etapas)": 2.0,
    "TBL - gRAT (Grupo)": 1.0,
    "TBL - iRAT (Individual)": 1.5,
    "Prova Teórica": 3.4,
    "Lab. Práticas Integradas": 0.7,
    "Lab. Morfofuncional": 1.4
}

st.info("💡 Insira sua nota de 0 a 10 em cada categoria. O sistema calculará o peso automaticamente.")

col1, col2 = st.columns([1, 1])
notas_finais = {}

with col1:
    st.markdown("### 📝 Notas Inseridas")
    for nome, peso_max in pesos.items():
        # Input de 0 a 10
        nota_input = st.text_input(f"{nome} (Vale {peso_max} pts)", value="", help=f"Quanto você tirou de 0 a 10 nesta categoria?")
        
        if nota_input:
            try:
                valor = float(nota_input.replace(',', '.'))
                # Cálculo da regra de três: (nota/10) * peso_max
                nota_final = (valor / 10) * peso_max
                notas_finais[nome] = nota_final
            except ValueError:
                st.error(f"Insira um número válido para {nome}")

with col2:
    st.markdown("### 📊 Resultado Parcial")
    
    nota_total = sum(notas_finais.values())
    pontos_preenchidos = sum([pesos[k] for k in notas_finais.keys()])
    pontos_faltantes = 10.0 - pontos_preenchidos
    
    # Card de Nota Atual
    st.markdown(f"""
        <div class="metric-card">
            <p style='margin:0; color: #666;'>Sua Pontuação Acumulada</p>
            <h2 style='margin:0; color: #2e5a88;'>{nota_total:.2f} / 10.0</h2>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    
    if pontos_preenchidos > 0:
        media_aprovacao = 7.0 # Geralmente medicina é 7, ajuste se necessário
        
        if nota_total >= media_aprovacao:
            st.success(f"⭐ Parabéns! Você já atingiu a média {media_aprovacao}!")
            st.balloons()
        elif pontos_faltantes > 0:
            falta_para_passar = media_aprovacao - nota_total
            if falta_para_passar > pontos_faltantes:
                st.error(f"Atenção: Mesmo gabaritando o que resta ({pontos_faltantes:.2f}), você somaria {nota_total + pontos_faltantes:.2f}. Procure o professor sobre a prova final.")
            else:
                st.warning(f"Faltam **{falta_para_passar:.2f} pontos** para atingir a média {media_aprovacao}.")
                # Calculando o rendimento necessário nas próximas
                rendimento = (falta_para_passar / pontos_faltantes) * 10
                st.write(f"Você precisa de um aproveitamento de **{rendimento:.1f} nas próximas avaliações**.")
    else:
        st.write("Aguardando as primeiras notas...")

# Detalhamento Visual
if notas_finais:
    with st.expander("Ver detalhamento por peso"):
        for nome, valor in notas_finais.items():
            st.write(f"**{nome}:** {valor:.2f} de {pesos[nome]} possíveis.")
