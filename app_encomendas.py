import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import os
import base64

st.set_page_config(
    page_title="Salgados Oliveira",
    page_icon="🥟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
:root {
    --primary: #FF6B35;
    --secondary: #F7931E;
}
.main {
    background: linear-gradient(135deg, #FFF5F0 0%, #FFE8D6 100%);
}
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    border-left: 4px solid var(--primary);
    margin-bottom: 15px;
}
.stButton>button {
    border-radius: 10px;
    border: none;
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    color: white;
    font-weight: 600;
    padding: 12px 24px;
    transition: all 0.3s;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(255,107,53,0.3);
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: white;
    padding: 10px;
    border-radius: 15px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    color: white;
}
h1 {
    color: #2E2E2E;
    font-weight: 700;
}
.login-container {
    max-width: 400px;
    margin: 50px auto;
    padding: 40px;
    background: white;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
@media print {
 .stButton,.stTabs,header,footer,.stSidebar,[data-testid="stToolbar"],.element-container:has(.stButton) {
        display: none!important;
    }
 .main {
        background: white!important;
    }
}
</style>
""", unsafe_allow_html=True)

ARQUIVO_CSV = "encomendas.csv"
LOGO_PATH = "logo.png"

SALGADOS = [
    'Coxinha', 'Pastel de frango', 'Pastel doce', 'Pastel de queijo',
    'Pastel misto', 'Pastel de carne', 'Canudos de frango',
    'Canudos de carne', 'Canudos de frango c/ azeitona e maionese',
    'Tortelete de frango', 'Tortelete doce', 'Empada',
    'Salgadinho de queijo assado', 'Salgadinho de queijo frito',
    'Bolinha empanada de azeitona e queijo', 'Bolinha empanada de queijo',
    'Bolinha empanada de charque', 'Mini pizzas', 'Pastel mercado'
]

FORMAS_PAGAMENTO = ['A vista', 'Cartão de crédito', 'Cartão de débito', 'Pix', 'Fiado']

def salvar_dados(df):
    df.to_csv(ARQUIVO_CSV, index=False)

def atualizar_status_automatico(df):
    if df.empty:
        return df
    agora = datetime.now()
    alterou = False
    for idx, row in df.iterrows():
        if row['Status'] not in ['Entregue', 'Cancelada']:
            try:
                data_str = f"{row['Data_Entrega']} {row['Hora_Entrega']}"
                data_entrega = datetime.strptime(data_str, '%d/%m/%Y %H:%M')
                if agora > data_entrega:
                    df.loc[idx, 'Status'] = 'Entregue'
                    alterou = True
            except:
                pass
    if alterou:
        salvar_dados(df)
    return df

def carregar_dados():
    colunas = ['Data_Pedido', 'Cliente', 'Telefone', 'Produto', 'Quantidade',
               'Valor', 'Data_Entrega', 'Hora_Entrega', 'Status', 'Observacoes', 'Forma_Pagamento']
    try:
        if os.path.exists(ARQUIVO_CSV) and os.path.getsize(ARQUIVO_CSV) > 0:
            df = pd.read_csv(ARQUIVO_CSV)
            if df.empty:
                return pd.DataFrame(columns=colunas)
            df = atualizar_status_automatico(df)
            return df
    except:
        pass
    df_vazio = pd.DataFrame(columns=colunas)
    df_vazio.to_csv(ARQUIVO_CSV, index=False)
    return df_vazio

def card_metrica(titulo, valor, icone, cor):
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: {cor};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <p style="color: #888; font-size: 14px; margin: 0;">{titulo}</p>
                <h2 style="color: #2E2E2E; margin: 5px 0 0 0;">{valor}</h2>
            </div>
            <div style="font-size: 40px;">{icone}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def gerar_pdf_download(df, nome_arquivo):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{nome_arquivo}">📥 Baixar CSV</a>'
    return href

def botao_imprimir():
    st.markdown("""
    <button onclick="window.print()" style="
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
    ">🖨️ Imprimir Página</button>
    """, unsafe_allow_html=True)

def login():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=150)
        st.markdown('<h1 style="text-align: center; color:                                                                
        st.markdown('#FF6B35;">🥟 Salgados Oliveira</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color:                                                                      
        st.markdown("#888;">Sistema de Gestão de Encomendas</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("login_form"):
            usuario = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
            entrar = st.form_submit_button("Entrar", use_container_width=True)
            if entrar:
                if usuario == "admin" and senha == "admin123":
                    st.session_state['logado'] = True
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha incorretos!")
        st.markdown('</div>', unsafe_allow_html=True)

def editar_encomenda(index, df):
    st.subheader("editar_encomenda(index, df):
    st.subheader("✏️ Editar Encomenda")
    row = df.loc[index]
    with st.form("editar_encomenda"):
        cliente = st.text_input("Cliente", value=row['Cliente'])
        telefone = st.text_input("Telefone", value=row['Telefone'])
        produto = st.text_input("Produto", value=row['Produto'])
        quantidade = st.number_input("Quantidade", value=int(row['Quantidade']), min_value=1)
        valor = st.number_input("Valor", value=float(row['Valor']), min_value=0.0, format="%.2f")
        data_entrega = st.date_input("Data Entrega", value=datetime.strptime(row['Data_Entrega'], '%d/%m/%Y'))
        hora_entrega = st.time_input("Hora Entrega", value=datetime.strptime(row['Hora_Entrega'], '%H:%M'))
        status = st.selectbox("Status", ['Pendente', 'Em produção', 'Pronto', 'Entregue', 'Cancelada'], index=['Pendente', 'Em produção', 'Pronto', 'Entregue', 'Cancelada'].index(row['Status']))
        forma_pagamento = st.selectbox("Forma de
