import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import os
import urllib.parse

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Salgados Oliveira",
    page_icon="🥟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS CUSTOMIZADO
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
</style>
""", unsafe_allow_html=True)

ARQUIVO_CSV = "encomendas.csv"
LOGO_PATH = "logo.png"

# LISTA DE SALGADOS
SALGADOS = [
    'Coxinha', 'Pastel de frango', 'Pastel doce', 'Pastel de queijo',
    'Pastel misto', 'Pastel de carne', 'Canudos de frango',
    'Canudos de carne', 'Canudos de frango c/ azeitona e maionese',
    'Tortelete de frango', 'Tortelete doce', 'Empada',
    'Salgadinho de queijo assado', 'Salgadinho de queijo frito',
    'Bolinha empanada de azeitona e queijo', 'Bolinha empanada de queijo',
    'Bolinha empanada de charque', 'Mini pizzas', 'Pastel mercado'
]

# FUNÇÕES AUXILIARES
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
    if os.path.exists(ARQUIVO_CSV) and os.path.getsize(ARQUIVO_CSV) > 0:
        try:
            df = pd.read_csv(ARQUIVO_CSV)
            df = atualizar_status_automatico(df)
            return df
        except pd.errors.EmptyDataError:
            pass
    df_vazio = pd.DataFrame(columns=[
        'Data_Pedido', 'Cliente', 'Telefone', 'Produto', 'Quantidade',
        'Valor', 'Data_Entrega', 'Hora_Entrega', 'Status', 'Observacoes'
    ])
    df_vazio.to_csv(ARQUIVO_CSV, index=False)
    return df_vazio

def salvar_dados(df):
    df.to_csv(ARQUIVO_CSV, index=False)

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

# TELA DE LOGIN
def login():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=150)
        st.markdown("<h1 style='text-align: center; color:                                                                
        st.markdown("#FF6B35;'>🥟 Salgados Oliveira</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color:                                                                      
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("login_form"):
            usuario = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
            entrar = st.form_submit_button("Entrar", use_container_width=True)
            if entrar:
                if usuario == "admin" and senha == "admin123":
                    st.session_state['#888;'>Sistema de Gestão de Encomendas</p>", unsafe_allow_html=True)
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

               
def app_principal():
    if '# APP PRINCIPAL
def app_principal():
    if 'produtos' not in st.session_state:
        st.session_state.produtos = []

            
    col1, col2, col3 = st.columns([1,3,1])
    with col1:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=80)
    with col2:
        st.markdown("<h1 style='# HEADER
    col1, col2, col3 = st.columns([1,3,1])
    with col1:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=80)
    with col2:
        st.markdown("<h1 style='text-align: center; margin: 0;'>🥟 Salgados Oliveira</h1>", unsafe_allow_html=True)
    with col3:
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state['logado'] = False
            st.rerun()
    st.markdown("---")

          
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", "➕ Nova", "📋 Ver", "✏️ Editar", "🗑️ Excluir"
    ])

                       
    with tab1:
        df = carregar_dados()
        if df.empty:
            st.info("📭 Nenhuma encomenda cadastrada ainda. Vá em '# ABAS
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", "➕ Nova", "📋 Ver", "✏️ Editar", "🗑️ Excluir"
    ])

    # ABA 1 - DASHBOARD
    with tab1:
        df = carregar_dados()
        if df.empty:
            st.info("📭 Nenhuma encomenda cadastrada ainda. Vá em 'Nova' para começar.")
        else:
            df['Data_Entrega_dt'] = pd.to_datetime(df['Data_Entrega'], format='%d/%m/%Y', errors='coerce')
            hoje = date.today()
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            fat_hoje = df[(df['Data_Entrega_dt'].dt.date == hoje) & (~df['Status'].isin(['Entregue', 'Cancelada']))]['Valor'].sum()
            fat_semana = df[(df['Data_Entrega_dt'].dt.date >= inicio_semana) & (~df['Status'].isin(['Entregue', 'Cancelada']))]['Valor'].sum()
            fat_total = df[df['Status'] == 'Entregue']['Valor'].sum()
            pedidos_pendentes = len(df[df['Status'].isin(['Pendente', 'Em produção', 'Pronto'])])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                card_metrica("Hoje", f"R$ {fat_hoje:.2f}", "💰", "#FF6B35")
