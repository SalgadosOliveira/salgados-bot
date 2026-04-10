import streamlit as st
from datetime import date

st.set_page_config(page_title="Salgados Oliveira", page_icon="🥟")
st.title("🥟 Salgados Oliveira")
st.subheader("Sistema de Encomendas")

nome = st.text_input("Nome do cliente")
telefone = st.text_input("Telefone")
data_entrega = st.date_input("Data da entrega", min_value=date.today())

col1, col2 = st.columns(2)
with col1:
    coxinha = st.number_input("Coxinha", 0, step=10)
    pastel = st.number_input("Pastel", 0, step=10)
with col2:
    kibe = st.number_input("Kibe", 0, step=10)
    empada = st.number_input("Empada", 0, step=10)

if st.button("Registrar"):
    total = coxinha + pastel + kibe + empada
    if nome and total > 0:
        st.success(f"Encomenda de {total} salgados registrada para {nome}!")
        st.balloons()
    else:
        st.error("Preencha nome e adicione salgados")
