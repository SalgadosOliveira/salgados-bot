import streamlit as st
import pandas as pd
from datetime import datetime, date

# Configurações
st.set_page_config(
    page_title="Salgados Oliveira - Encomendas", 
    page_icon="🥟",
    layout="wide"
)

# CSS customizado laranja + preto
st.markdown("""
<style>
    .stApp {
        background-color: #f5f5f5;
    }
    .main > div {
        padding-top: 2rem;
    }
    h1, h2, h3 {
        color: #1a1a1a !important;
        font-weight: 700;
    }
    .stButton>button {
        background-color: #FF6600;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #E55A00;
        color: white;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stDateInput>div>div>input {
        border-radius: 8px;
    }
    hr {
        border-color: #FF6600;
    }
</style>
""", unsafe_allow_html=True)

# Header com logo
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    st.image("https://via.placeholder.com/80x80.png?text=LOGO", width=80)  # TROCA PELA URL DO SEU LOGO
with col_titulo:
    st.title("Salgados Oliveira")
    st.caption("Sistema de Encomendas")

st.markdown("<hr style='border:2px solid #FF6600'>", unsafe_allow_html=True)

# Dados
if 'encomendas' not in st.session_state:
    st.session_state.encomendas = []

# Formulário
with st.container():
    st.subheader("📝 Nova Encomenda")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        nome = st.text_input("Nome do cliente *")
    with col2:
        telefone = st.text_input("Telefone/WhatsApp *")
    with col3:
        data_entrega = st.date_input("Data da entrega *", min_value=date.today())
    
    st.markdown("##### Salgados - Mínimo 10 unidades")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        coxinha = st.number_input("Coxinha", min_value=0, step=10, value=0)
        pastel = st.number_input("Pastel", min_value=0, step=10, value=0)
    with c2:
        kibe = st.number_input("Kibe", min_value=0, step=10, value=0)
        empada = st.number_input("Empada", min_value=0, step=10, value=0)
    with c3:
        bolinha_queijo = st.number_input("Bolinha de Queijo", min_value=0, step=10, value=0)
        risole = st.number_input("Risole", min_value=0, step=10, value=0)
    
    obs = st.text_area("Observações")
    
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    with col_b1:
        if st.button("✅ Registrar", use_container_width=True):
            salgados = {"Coxinha": coxinha, "Pastel": pastel, "Kibe": kibe, 
                       "Empada": empada, "Bolinha de Queijo": bolinha_queijo, "Risole": risole}
            total = sum(salgados.values())
            if nome and telefone and total >= 10:
                st.session_state.encomendas.append({
                    "ID": len(st.session_state.encomendas),
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Cliente": nome,
                    "Telefone": telefone,
                    "Entrega": data_entrega.strftime("%d/%m/%Y"),
                    "Salgados": salgados,
                    "Total": total,
                    "Obs": obs,
                    "Status": "Pendente"
                })
                st.success(f"Encomenda de {total} salgados registrada!")
                st.balloons()
            elif total < 10:
                st.warning("Pedido mínimo: 10 salgados")
            else:
                st.error("Preencha nome e telefone")
    
    with col_b2:
        if st.button("🖨️ Imprimir", use_container_width=True):
            st.info("Função de impressão em desenvolvimento")
    
    with col_b3:
        if st.button("📊 Rel. Semanal", use_container_width=True):
            st.info("Relatório semanal em desenvolvimento")
    
    with col_b4:
        if st.button("📈 Rel. Mensal", use_container_width=True):
            st.info("Relatório mensal em desenvolvimento")

st.markdown("<hr style='border:2px solid #FF6600'>", unsafe_allow_html=True)

# Lista de encomendas
st.subheader("📦 Encomendas Registradas")

if st.session_state.encomendas:
    # Atualiza status automático: se passou da data vira Entregue
    hoje = date.today()
    for enc in st.session_state.encomendas:
        data_entrega = datetime.strptime(enc["Entrega"], "%d/%m/%Y").date()
        if data_entrega < hoje and enc["Status"] == "Pendente":
            enc["Status"] = "Entregue"
    
    # Separa pendentes e entregues
    pendentes = [e for e in st.session_state.encomendas if e["Status"] == "Pendente"]
    entregues = [e for e in st.session_state.encomendas if e["Status"] == "Entregue"]
    
    tab1, tab2 = st.tabs(["⏳ Pendentes", "✅ Entregues"])
    
    with tab1:
        if pendentes:
            for enc in pendentes:
                with st.container():
                    st.markdown(f"#### {enc['Cliente']} - {enc['Telefone']}")
                    c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
                    with c1:
                        st.write(f"**Entrega:** {enc['Entrega']} | **Total:** {enc['Total']} salgados")
                        salgados_txt = ", ".join([f"{k}: {v}" for k, v in enc["Salgados"].items() if v > 0])
                        st.caption(salgados_txt)
                    with c2:
                        if st.button("✅ Marcar Entregue", key=f"ent_{enc['ID']}", use_container_width=True):
                            enc["Status"] = "Entregue"
                            st.rerun()
                    with c3:
                        if st.button("👁️ Ver", key=f"ver_{enc['ID']}", use_container_width=True):
                            st.json(enc)
                    with c4:
                        if st.button("🗑️ Excluir", key=f"del_{enc['ID']}", use_container_width=True):
                            st.session_state.encomendas = [e for e in st.session_state.encomendas if e["ID"] != enc["ID"]]
                            st.rerun()
                    st.divider()
        else:
            st.info("Nenhuma encomenda pendente")
    
    with tab2:
        if entregues:
            df_ent = pd.DataFrame(entregues)
            st.dataframe(df_ent[["Cliente", "Telefone", "Entrega", "Total", "Obs"]], use_container_width=True)
        else:
            st.info("Nenhuma encomenda entregue ainda")
else:
    st.info("Nenhuma encomenda registrada ainda")

st.markdown("<hr style='border:2px solid #FF6600'>", unsafe_allow_html=True)
st.caption("Salgados Oliveira © 2026 - São José do Egito, PE")
