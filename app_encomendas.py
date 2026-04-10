import streamlit as st
import pandas as pd
from datetime import datetime, date

# Configurações da página
st.set_page_config(
    page_title="Salgados Oliveira - Encomendas", 
    page_icon="🥟",
    layout="wide"
)

# Título
st.title("🥟 Salgados Oliveira")
st.subheader("Sistema de Encomendas")
st.write("---")

# Dados
if 'encomendas' not in st.session_state:
    st.session_state.encomendas = []

# Funções
def salvar_encomenda(nome, telefone, data_entrega, salgados, obs):
    st.session_state.encomendas.append({
        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Cliente": nome,
        "Telefone": telefone,
        "Entrega": data_entrega.strftime("%d/%m/%Y"),
        "Salgados": salgados,
        "Obs": obs,
        "Status": "Pendente"
    })

# Formulário
with st.container():
    st.header("📝 Nova Encomenda")
    nome = st.text_input("Nome do cliente *")
    telefone = st.text_input("Telefone/WhatsApp *")
    data_entrega = st.date_input("Data da entrega *", min_value=date.today())
    
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
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Registrar Encomenda", use_container_width=True):
            if nome and telefone:
                salgados = {
                    "Coxinha": coxinha,
                    "Pastel": pastel,
                    "Kibe": kibe,
                    "Empada": empada,
                    "Bolinha de Queijo": bolinha_queijo,
                    "Risole": risole
                }
                total = sum(salgados.values())
                if total >= 10:
                    salvar_encomenda(nome, telefone, data_entrega, salgados, obs)
                    st.success(f"Encomenda registrada para {nome}!")
                    st.balloons()
                else:
                    st.warning("Pedido mínimo: 10 salgados")
            else:
                st.error("Preencha nome e telefone")
    
    with col2:
        if st.button("📄 Imprimir Pedido", use_container_width=True):
            st.write("Função de impressão aqui...")
    
    with col3:
        if st.button("❌ Cancelar", use_container_width=True):
            st.session_state.encomendas = []
            st.warning("Todas as encomendas foram canceladas")

# Lista de encomendas
st.write("---")
st.header("📦 Encomendas Registradas")

if st.session_state.encomendas:
    df = pd.DataFrame(st.session_state.encomendas)
    st.dataframe(df, use_container_width=True)
    
    # Relatórios
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Relatório Semanal", use_container_width=True):
            st.write("Relatório semanal...")
    with col2:
        if st.button("📈 Relatório Mensal", use_container_width=True):
            st.write("Relatório mensal...")
else:
    st.info("Nenhuma encomenda registrada ainda")

st.write("---")
st.caption("Salgados Oliveira © 2026 - São José do Egito, PE")
