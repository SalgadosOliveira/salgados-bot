import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Salgados Oliveira - Encomendas", page_icon="🥟")

st.title("🥟 Salgados Oliveira")
st.subheader("Sistema de Encomendas")

st.write("---")

st.header("Fazer Nova Encomenda")

nome = st.text_input("Nome do cliente")
telefone = st.text_input("Telefone/WhatsApp")
data_entrega = st.date_input("Data da entrega", min_value=datetime.today())

st.subheader("Salgados")
col1, col2 = st.columns(2)

with col1:
    coxinha = st.number_input("Coxinha", min_value=0, step=10)
    pastel = st.number_input("Pastel", min_value=0, step=10)
    kibe = st.number_input("Kibe", min_value=0, step=10)

with col2:
    empada = st.number_input("Empada", min_value=0, step=10)
    bolinha_queijo = st.number_input("Bolinha de Queijo", min_value=0, step=10)
    risole = st.number_input("Risole", min_value=0, step=10)

obs = st.text_area("Observações")

if st.button("Registrar Encomenda"):
    if nome and telefone:
        total = coxinha + pastel + kibe + empada + bolinha_queijo + risole
        if total > 0:
            st.success(f"Encomenda registrada para {nome}!")
            st.balloons()
            
            encomenda = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Cliente": nome,
                "Telefone": telefone,
                "Entrega": data_entrega.strftime("%d/%m/%Y"),
                "Coxinha": coxinha,
                "Pastel": pastel,
                "Kibe": kibe,
                "Empada": empada,
                "Bolinha de Queijo": bolinha_queijo,
                "Risole": risole,
                "Total": total,
                "Obs": obs
            }
            st.write("Resumo:", encomenda)
        else:
            st.warning("Adicione pelo menos 1 salgado")
    else:
        st.error("Preencha nome e telefone")

st.write("---")
st.caption("Salgados Oliveira © 2026")
