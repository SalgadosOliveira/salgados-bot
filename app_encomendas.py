import streamlit as st
import pandas as pd
from datetime import datetime, date

# Configurações
st.set_page_config(
    page_title="Salgados Oliveira - Encomendas", 
    page_icon="🥟",
    layout="wide"
)

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

def marcar_entregue(index):
    if index < len(st.session_state.encomendas):
        st.session_state.encomendas[index]["Status"] = "Entregue"

def excluir_encomenda(index):
    if index < len(st.session_state.encomendas):
        st.session_state.encomendas.pop(index)

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

# Lista de encomendas
st.write("---")
st.header("📦 Encomendas")

if st.session_state.encomendas:
    # Atualiza status automaticamente
    hoje = date.today()
    for i, enc in enumerate(st.session_state.encomendas):
        data_entrega = datetime.strptime(enc["Entrega"], "%d/%m/%Y").date()
        if data_entrega < hoje and enc["Status"] == "Pendente":
            st.session_state.encomendas[i]["Status"] = "Entregue"
    
    df = pd.DataFrame(st.session_state.encomendas)
    st.dataframe(df, use_container_width=True)
    
    # Ações
    for i, enc in enumerate(st.session_state.encomendas):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button(f"👀 Ver {i}", use_container_width=True):
                st.write(enc)
        with col2:
            if st.button(f"✏️ Editar {i}", use_container_width=True):
                st.write("Editar aqui...")
        with col3:
            if st.button(f"✅ Entregue {i}", use_container_width=True):
                marcar_entregue(i)
                st.rerun()
        with col4:
            if st.button(f"🗑️ Excluir {i}", use_container_width=True):
                excluir_encomenda(i)
                st.rerun()
else:
    st.info("Nenhuma encomenda registrada ainda")

st.write("---")
st.caption("Salgados Oliveira © 2026 - São José do Egito, PE")
