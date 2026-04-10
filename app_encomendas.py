import streamlit as st
import pandas as pd
from datetime import datetime, date

# Configurações
st.set_page_config(
    page_title="Salgados Oliveira - Encomendas", 
    page_icon="🥟",
    layout="wide"
)

# CSS customizado
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton>button {
        background-color: #ff6600;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #e65c00;
    }
    h1, h2, h3 {
        color: #333333;
    }
    .card {
        background-color: white;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header com logo
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://via.placeholder.com/100x100", width=100)  # Coloca a URL do seu logo aqui
with col2:
    st.title("🥟 Salgados Oliveira")
    st.subheader("Sistema de Encomendas")

st.write("---")

# Restante do código...
